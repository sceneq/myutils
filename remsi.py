#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations
import re
from typing import TextIO

quote_double = lambda s: '"' + s + '"'
quote_single = lambda s: "'" + s + "'"


def doit(
    ffmpeg_output: str,
    only_silence=False,
):
    silence_start_pat = re.compile(r"silence_start: (\d+\.?\d+)")
    silence_end_pat = re.compile(r"silence_end: (\d+\.?\d+)")

    if only_silence:
        silence_start_pat, silence_end_pat = silence_start_pat, silence_end_pat

    starts = silence_start_pat.findall(ffmpeg_output)
    ends = silence_end_pat.findall(ffmpeg_output)
    selections = [f"between(t,{e},{s})" for s, e in zip(starts, [0] + ends)]

    if (m:=re.search(r"Input .+ from '(.+)':", ffmpeg_output[:1000])) is not None:
        input_file = m.group(1)
    else:
        raise ValueError

    # ノイズなし
    if len(selections) == 0:
        return input_file, "", ""

    selection_filter = quote_single("+".join(selections))
    vfilter = "-filter:v " + quote_double(f"select={selection_filter},setpts=N/FRAME_RATE/TB")
    afilter = "-filter:a " + quote_double(f"aselect={selection_filter},asetpts=N/SR/TB")

    return input_file, vfilter, afilter


def main():
    import sys

    outfile_path = sys.argv[1]
    input_file, vfilter, afilter = doit(sys.stdin.read())
    cmd = [
        "ffmpeg.exe",
        "-y",
        "-i",
        quote_double(input_file),
        vfilter,
        afilter,
        quote_double(outfile_path),
    ]
    print(" ".join(cmd))


def test(inp_path: str):
    outfile_path = "tmp"
    inp = open(inp_path, "r")
    input_file, vfilter, afilter = doit(inp.read())
    cmd = [
        "ffmpeg.exe",
        "-y",
        "-i",
        quote_double(input_file),
        vfilter,
        afilter,
        quote_double(outfile_path),
    ]
    print(" ".join(cmd))


if __name__ == "__main__":
    # main()
    test("./kogoe_-50db1d.mp4.txt")
    # test("./kogoe_-26db1d.mp4.txt")
