#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import re


@dataclass
class LogEntry:
    timestamp: datetime
    message: str


class LogParser:
    def __init__(self):
        self.entries: list[LogEntry] = []
        self.current_date: datetime | None = None

    def parse(self, text: str) -> list[LogEntry]:
        for line in text.splitlines():
            if match := re.match(r"(\d{4}/\d{1,2}/\d{1,2})", line):
                # New date, update current_date
                self.current_date = datetime.strptime(match.group(1), "%Y/%m/%d")
            elif match := re.match(r"(\d{1,2}):(\d{1,2})(?: (.+)|$)", line):
                # Timestamp and message, combine with current_date
                hour, minute, message = match.groups()

                add_to_day = 0
                if int(hour) >= 24:
                    hour = int(hour) - 24
                    add_to_day = 1

                if self.current_date:
                    time = datetime(1900, 1, 1, hour=int(hour), minute=int(minute))
                    date = self.current_date + timedelta(days=add_to_day)
                    timestamp = datetime.combine(date, time.time())
                    log = LogEntry(timestamp=timestamp, message=message or "")
                    self.entries.append(log)
            else:
                # Multiline message continuation
                if self.entries:
                    self.entries[-1].message += "\n" + line

        return self.entries


#
#
#
import sys
import re
from pathlib import Path
from argparse import ArgumentParser

# 引数パーサーの設定
parser = ArgumentParser()
parser.add_argument("files", nargs="*", help="入力ファイル")
parser.add_argument("-f", "--filter", help="message フィールドに対する正規表現フィルタ")

args = parser.parse_args()

# ファイルの決定
if len(args.files) == 0:
    input_files = [Path("/mnt/c/Users/iiiii/Documents/Mega/memo/android/日記.txt")]
else:
    input_files = list(map(Path, args.files))

# 正規表現フィルタの準備（指定されていれば）
filter_pattern = re.compile(args.filter) if args.filter else None

i = 0
for inp in input_files:
    nikki = inp.read_text(encoding="utf-8")  # encodingは適宜
    parser = LogParser()
    parsed_entries = parser.parse(nikki)

    for entry in parsed_entries:
        message = entry.message
        if filter_pattern is None or filter_pattern.search(message):
            i += 1
            print(
                # entry.timestamp.strftime("%Y/%m/%d %H:%M"),
                f"{i}. "
                + repr(entry.message),
            )
