#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Pillow==11.2.1",
# ]
# ///

from __future__ import annotations
from PIL import Image, ImageDraw


def create_vertical_4koma(
    image_path: str,
    output_path: str,
) -> None:
    original = Image.open(image_path)
    width, height = original.size
    panel_height = height // 4

    # パネル分割(上→下)
    panels = [
        original.crop((0, i * panel_height, width, (i + 1) * panel_height))
        for i in range(4)
    ]

    outer_margin = 40
    panel_margin = 50
    border_width = 6
    border_color = "black"
    title_height = 60

    # 出力画像サイズ
    output_width = width + 2 * outer_margin
    output_height = (
        title_height
        + 4 * panel_height
        + 3 * panel_margin  # パネルの高さ
        + 2 * outer_margin  # パネル間のマージン
    )

    canvas = Image.new("RGB", (output_width, output_height), color="white")
    draw = ImageDraw.Draw(canvas)

    for i, panel in enumerate(panels):
        x = outer_margin
        y = title_height + outer_margin + i * (panel_height + panel_margin)

        # 枠線
        draw.rectangle(
            [
                x - border_width,
                y - border_width,
                x + width + border_width,
                y + panel_height + border_width,
            ],
            outline=border_color,
            width=border_width,
        )

        canvas.paste(panel, (x, y))

    canvas.save(output_path)


create_vertical_4koma("ごくせん.jpg", "out.jpg")
