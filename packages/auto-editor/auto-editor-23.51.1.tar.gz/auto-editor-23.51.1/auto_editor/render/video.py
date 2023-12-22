from __future__ import annotations

import os.path
from dataclasses import dataclass
from math import ceil
from subprocess import DEVNULL, PIPE
from typing import TYPE_CHECKING

import av
from PIL import Image, ImageOps

from auto_editor.output import video_quality
from auto_editor.render.image import make_cache, render_image
from auto_editor.timeline import TlVideo
from auto_editor.utils.encoder import encoders

if TYPE_CHECKING:
    from typing import Any

    from auto_editor.ffwrapper import FFmpeg, FileInfo
    from auto_editor.timeline import v3
    from auto_editor.utils.bar import Bar
    from auto_editor.utils.container import Container
    from auto_editor.utils.log import Log
    from auto_editor.utils.types import Args

av.logging.set_level(av.logging.PANIC)


@dataclass(slots=True)
class VideoFrame:
    index: int
    src: FileInfo


# From: github.com/PyAV-Org/PyAV/blob/main/av/video/frame.pyx
allowed_pix_fmt = {
    "yuv420p",
    "yuvj420p",
    "rgb48be",
    "rgb48le",
    "rgb64be",
    "rgb64le",
    "rgb24",
    "bgr24",
    "argb",
    "rgba",
    "abgr",
    "bgra",
    "gray",
    "gray8",
    "gray16be",
    "gray16le",
    "rgb8",
    "bgr8",
    "pal8",
}


def render_av(
    ffmpeg: FFmpeg,
    tl: v3,
    args: Args,
    bar: Bar,
    ctr: Container,
    temp: str,
    log: Log,
) -> tuple[str, bool]:
    src = tl.src
    img_cache = make_cache(tl.v)

    cns: dict[FileInfo, av.container.InputContainer] = {}
    decoders: dict[FileInfo, Any] = {}
    seek_cost: dict[FileInfo, int] = {}
    tous: dict[FileInfo, int] = {}

    target_pix_fmt = "yuv420p"  # Reasonable default

    first_src: FileInfo | None = None
    for src in tl.sources:
        if first_src is None:
            first_src = src

        if src not in cns:
            cns[src] = av.open(f"{src.path}")

    for src, cn in cns.items():
        if len(cn.streams.video) == 0:
            decoders[src] = None
            tous[src] = 0
            seek_cost[src] = 0
        else:
            stream = cn.streams.video[0]
            stream.thread_type = "AUTO"

            if args.no_seek or stream.average_rate is None or stream.time_base is None:
                sc_val = 4294967295  # 2 ** 32 - 1
                tou = 0
            else:
                # Keyframes are usually spread out every 5 seconds or less.
                sc_val = int(stream.average_rate * 5)
                tou = int(stream.time_base.denominator / stream.average_rate)

            seek_cost[src] = sc_val
            tous[src] = tou
            decoders[src] = cn.decode(stream)

            if src == first_src and stream.pix_fmt is not None:
                target_pix_fmt = stream.pix_fmt

    log.debug(f"Tous: {tous}")
    log.debug(f"Clips: {tl.v}")

    target_pix_fmt = target_pix_fmt if target_pix_fmt in allowed_pix_fmt else "yuv420p"
    log.debug(f"Target pix_fmt: {target_pix_fmt}")

    apply_video_later = True

    if args.scale != 1:
        apply_video_later = False
    elif args.video_codec in encoders:
        apply_video_later = set(encoders[args.video_codec]).isdisjoint(allowed_pix_fmt)

    log.debug(f"apply video quality settings now: {not apply_video_later}")

    width, height = tl.res
    spedup = os.path.join(temp, "spedup0.mp4")

    cmd = [
        "-hide_banner",
        "-y",
        "-f",
        "rawvideo",
        "-c:v",
        "rawvideo",
        "-pix_fmt",
        target_pix_fmt,
        "-s",
        f"{width}*{height}",
        "-framerate",
        f"{tl.tb}",
        "-i",
        "-",
        "-pix_fmt",
        target_pix_fmt,
    ]

    if apply_video_later:
        cmd += ["-c:v", "mpeg4", "-qscale:v", "1"]
    else:
        cmd += video_quality(args, ctr)

    # Setting SAR requires re-encoding so we do it here.
    if src is not None and src.videos and (sar := src.videos[0].sar) is not None:
        cmd.extend(["-vf", f"setsar={sar}"])

    cmd.append(spedup)

    process2 = ffmpeg.Popen(cmd, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL)
    assert process2.stdin is not None

    # First few frames can have an abnormal keyframe count, so never seek there.
    seek = 10

    seek_frame = None
    frames_saved = 0

    bar.start(tl.end, "Creating new video")

    null_img = Image.new("RGB", (width, height), args.background)
    null_frame = av.VideoFrame.from_image(null_img).reformat(format=target_pix_fmt)

    frame_index = -1
    frame = null_frame
    try:
        for index in range(tl.end):
            # Add objects to obj_list
            obj_list: list[Any] = []
            for layer in tl.v:
                for lobj in layer:
                    if isinstance(lobj, TlVideo):
                        if index >= lobj.start and index < (lobj.start + lobj.dur):
                            _i = lobj.offset + round((index - lobj.start) * lobj.speed)
                            obj_list.append(VideoFrame(_i, lobj.src))
                    elif index >= lobj.start and index < lobj.start + lobj.dur:
                        obj_list.append(lobj)

            # Render obj_list
            for obj in obj_list:
                if isinstance(obj, VideoFrame):
                    my_stream = cns[obj.src].streams.video[0]
                    if frame_index > obj.index:
                        log.debug(f"Seek: {frame_index} -> 0")
                        cns[obj.src].seek(0)
                        try:
                            assert decoders[obj.src] is not None
                            frame = next(decoders[obj.src])
                            frame_index = round(frame.time * tl.tb)
                        except StopIteration:
                            pass

                    while frame_index < obj.index:
                        # Check if skipping ahead is worth it.
                        if (
                            obj.index - frame_index > seek_cost[obj.src]
                            and frame_index > seek
                        ):
                            seek = frame_index + (seek_cost[obj.src] // 2)
                            seek_frame = frame_index
                            log.debug(f"Seek: {frame_index} -> {obj.index}")
                            cns[obj.src].seek(
                                obj.index * tous[obj.src],
                                stream=my_stream,
                            )

                        try:
                            frame = next(decoders[obj.src])
                            frame_index = round(frame.time * tl.tb)
                        except StopIteration:
                            log.debug(f"No source frame at {index=}. Using null frame")
                            frame = null_frame
                            break

                        if seek_frame is not None:
                            log.debug(
                                f"Skipped {frame_index - seek_frame} frame indexes"
                            )
                            frames_saved += frame_index - seek_frame
                            seek_frame = None
                        if frame.key_frame:
                            log.debug(f"Keyframe {frame_index} {frame.pts}")

                    if frame.width != width or frame.height != height:
                        img = frame.to_image().convert("RGB")
                        if img.width > width or img.height > height:
                            factor = ceil(max(width / img.width, height / img.height))
                            img = ImageOps.scale(img, factor)
                        img = ImageOps.pad(img, (width, height), color=args.background)
                        frame = frame.from_image(img).reformat(format=target_pix_fmt)

                else:
                    frame = render_image(frame, obj, img_cache)

            if frame.format.name != target_pix_fmt:
                frame = frame.reformat(format=target_pix_fmt)
                bar.tick(index)
            elif index % 3 == 0:
                bar.tick(index)

            # if frame == null_frame:
            #     raise ValueError("no null frame allowed")

            process2.stdin.write(frame.to_ndarray().tobytes())

        bar.end()
        process2.stdin.close()
        process2.wait()
    except (OSError, BrokenPipeError):
        bar.end()
        ffmpeg.run_check_errors(cmd, log, True)
        log.error("FFmpeg Error!")

    log.debug(f"Total frames saved seeking: {frames_saved}")

    if args.scale != 1:
        sped_input = os.path.join(temp, "spedup0.mp4")
        spedup = os.path.join(temp, "scale0.mp4")
        scale_filter = f"scale=iw*{args.scale}:ih*{args.scale}"

        cmd = ["-i", sped_input, "-vf", scale_filter, spedup]

        check_errors = ffmpeg.pipe(cmd)
        if "Error" in check_errors or "failed" in check_errors:
            if "-allow_sw 1" in check_errors:
                cmd.insert(-1, "-allow_sw")
                cmd.insert(-1, "1")
            # Run again to show errors even if it might not work.
            ffmpeg.run(cmd)

    return spedup, apply_video_later
