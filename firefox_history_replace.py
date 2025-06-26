#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "furl==2.1.4",
# ]
# ///
# coding: utf-8

from furl import furl
import sqlite3
from sys import argv

#SQLITE_FILE = "./Data/Browser/profile.default/places.sqlite"
FROM_PREFIX = "http://"
TO_PREFIX = "http://"
#FROM_HOST = "a.com"
#TO_HOST = "new-a.com"

if len(argv) == 1:
    print(f"usage: <places.sqlite> <from-host> <to-host>")
    print(f"from-prefix={FROM_PREFIX}, to-prefix={TO_PREFIX}")
    exit(0)

SQLITE_FILE = argv[1]
FROM_HOST, TO_HOST = argv[2:]

MAX_INT = 2**32 - 1


def rotate_left_5(value):
    return ((value << 5) | (value >> 27)) & MAX_INT


def add_to_hash(hash_value, value):
    return (0x9E3779B9 * (rotate_left_5(hash_value) ^ value)) & MAX_INT


def hash_simple(url):
    hash_value = 0
    for char in url.encode('utf-8'):
        hash_value = add_to_hash(hash_value, char)
    return hash_value


def url_hash(url):
    prefix, _ = url.split(':', 1)
    return ((hash_simple(prefix) & 0x0000FFFF) << 32) + hash_simple(url)


def main():
    con = sqlite3.connect(SQLITE_FILE)

    origin_id, = con.execute(
        f"select id from moz_origins where prefix = '{FROM_PREFIX}' AND host = '{FROM_HOST}'"
    ).fetchone()
    q = f"select id, url from moz_places where url LIKE '{FROM_PREFIX}{FROM_HOST}%'"
    for id, url in con.execute(q):
        p = furl(url)
        p.set(host=TO_HOST, scheme=TO_PREFIX[:-3])
        new_url = p.url
        con.execute(
            """
        UPDATE moz_places
            SET
              url = ?,
              url_hash = ?,
              origin_id = ?
            where id = ?
        """, (new_url, url_hash(new_url), origin_id, id))
    con.commit()


if __name__ == "__main__":
    main()
