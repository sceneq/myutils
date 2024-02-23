#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from typing import DefaultDict
from dataclasses import dataclass
import statistics


@dataclass
class StraceRow:
    at: str
    syscall: str
    # args: list[str]
    elapsed: float


rows: list[StraceRow] = []
for line in Path("strace-T_fs_20230706091131.log").read_text().splitlines():
    time = line[:15]

    tmp = line[16:]
    arg_pare_pos = tmp.find("(")
    syscall = tmp[:arg_pare_pos]

    if syscall.startswith("+++ exited with "):
        continue

    elapsed_start_pos = line.rfind(" ")
    tmp = line[elapsed_start_pos + 2 : -1]
    if tmp == "":
        pass
    else:
        elapsed = float(tmp)
        rows.append(StraceRow(time, syscall, elapsed))


@dataclass
class Stat:
    num: int
    total: float
    avg: float
    stdev: float
    median: float


str_to_stat = {}

timemap: DefaultDict[str, list[float]] = defaultdict(lambda: [])
for r in rows:
    timemap[r.syscall].append(r.elapsed)
for key, value in timemap.items():
    num = len(value)
    total = sum(value)
    avg = total / num
    stdev = statistics.stdev(value) if num > 1 else 0.0
    median = statistics.median(value)
    str_to_stat[key] = Stat(num, total, avg, stdev, median)


print()
for key, stat in sorted(
    str_to_stat.items(), key=lambda item: item[1].total, reverse=True
)[:10]:
    print(f"{key}: {stat}")

print()
rows.sort(key=lambda r: r.elapsed, reverse=True)
for r in rows[:10]:
    print(r.syscall, r.elapsed)
