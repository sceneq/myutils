#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations
import random


def chars(fr: str, to: str) -> set[str]:
    return {chr(i) for i in range(ord(fr), ord(to) + 1)}


def generate_sum_list(
    count: int,
    target_sum: int,  # TODO
) -> list[int]:
    min_elements = 1
    if (count * min_elements) > target_sum:
        raise Exception
    tmp = [random.random() for _ in range(count)]
    tmp = [e / sum(tmp) * target_sum for e in tmp]
    tmp = [round(e) for e in tmp]
    return tmp


import typing

T = typing.TypeVar("T")


def arg(
    i: int,
    map_func: typing.Callable[[str], T] = str,
) -> T | None:
    import sys

    try:
        v = sys.argv[i]
        return map_func(v)
    except IndexError:
        return None


max_chars = arg(1, int) or 32
char_opt = (arg(2) or "alpha_numeric_symbol").lower()

charsets: list[list[str]] = []

if "al" in char_opt:
    charsets.append(list(chars("A", "Z") - {"I", "O"}))
    charsets.append(list(chars("a", "z") - {"l"}))
    char_opt = char_opt.replace("al", "")

if "num" in char_opt:
    charsets.append(list(chars("0", "9") - {"0"}))
    char_opt = char_opt.replace("num", "")

if "sym" in char_opt:
    # charsets.append(list("-_.=[]{}+#^!?:$/"))
    # charsets.append(list("-_.=[]{}+#^!?"))  # https://compas.arena.ne.jp/signup
    charsets.append(list("-_.=[]{}#^!?"))
    char_opt = char_opt.replace("sym", "")

if len(char_opt) >= 1:
    charsets.append([*char_opt])

password = [random.choice(charset) for charset in charsets]
remaining_chars = max_chars - len(password)
total_chars = sum(len(charset) for charset in charsets)
for i, charset in enumerate(charsets):
    chars_to_add = min(
        int(remaining_chars * (len(charset) / total_chars)), remaining_chars
    )
    password.extend(random.choices(charset, k=chars_to_add))
    remaining_chars -= chars_to_add
if remaining_chars > 0:
    all_chars = [char for charset in charsets for char in charset]
    password.extend(random.choices(all_chars, k=remaining_chars))

random.shuffle(password)
print("".join(password))
