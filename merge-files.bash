#!/usr/bin/env bash
set -o errexit -o errtrace -o noclobber -o pipefail -o nounset

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 file1 file2 [file3 ...] lastfile"
    exit 1
fi

lastfile="${!#}"

for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "Error: File $file does not exist."
        exit 1
    fi
done

# 最後のファイル以外の各ファイルに対してvimdiffを実行
for ((i=1; i<=$#-1; i++)); do
    if ! nvim -d "${!i}" "$lastfile"; then
        echo "Error: vimdiff failed for ${!i} and $lastfile"
        exit 1
    fi
done
