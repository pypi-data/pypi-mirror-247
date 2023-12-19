# -*- coding: utf-8 -*-
"""Contains helpers for watermark."""

from io import BytesIO
from typing import List, Union

from pdfrw import PageMerge, PdfReader
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from ..middleware.text import Text
from .utils import generate_stream


def draw_text(
    *args: Union[
        Canvas,
        Text,
        float,
        int,
        str,
    ]
) -> None:
    """Draws a text on the watermark."""

    canv = args[0]
    element = args[1]
    coordinate_x = args[2]
    coordinate_y = args[3]

    text_to_draw = element.value

    if not text_to_draw:
        text_to_draw = ""

    if element.max_length is not None:
        text_to_draw = text_to_draw[: element.max_length]

    canv.setFont(element.font, element.font_size)
    canv.setFillColorRGB(
        element.font_color[0], element.font_color[1], element.font_color[2]
    )

    if element.comb is True:
        for i, char in enumerate(text_to_draw):
            canv.drawString(
                coordinate_x + element.character_paddings[i],
                coordinate_y,
                char,
            )
    elif (
        element.text_wrap_length is None or len(text_to_draw) < element.text_wrap_length
    ) and element.text_lines is None:
        canv.drawString(
            coordinate_x,
            coordinate_y,
            text_to_draw,
        )
    else:
        text_obj = canv.beginText(0, 0)
        for i, line in enumerate(element.text_lines):
            cursor_moved = False
            if (
                element.text_line_x_coordinates is not None
                and element.text_line_x_coordinates[i] - coordinate_x != 0
            ):
                text_obj.moveCursor(
                    element.text_line_x_coordinates[i] - coordinate_x, 0
                )
                cursor_moved = True
            text_obj.textLine(line)
            if cursor_moved:
                text_obj.moveCursor(
                    -1 * (element.text_line_x_coordinates[i] - coordinate_x), 0
                )

        canv.saveState()
        canv.translate(
            coordinate_x,
            coordinate_y,
        )
        canv.drawText(text_obj)
        canv.restoreState()


def draw_image(*args: Union[Canvas, bytes, float, int]) -> None:
    """Draws an image on the watermark."""

    canv = args[0]
    image_stream = args[1]
    coordinate_x = args[2]
    coordinate_y = args[3]
    width = args[4]
    height = args[5]

    image_buff = BytesIO()
    image_buff.write(image_stream)
    image_buff.seek(0)

    canv.drawImage(
        ImageReader(image_buff),
        coordinate_x,
        coordinate_y,
        width=width,
        height=height,
    )

    image_buff.close()


def create_watermarks_and_draw(
    pdf: bytes,
    page_number: int,
    action_type: str,
    actions: List[
        List[
            Union[
                bytes,
                float,
                int,
                Text,
                str,
            ]
        ]
    ],
) -> List[bytes]:
    """Creates a canvas watermark and draw some stuffs on it."""

    pdf_file = PdfReader(fdata=pdf)
    buff = BytesIO()

    canv = Canvas(
        buff,
        pagesize=(
            float(pdf_file.pages[page_number - 1].MediaBox[2]),
            float(pdf_file.pages[page_number - 1].MediaBox[3]),
        ),
    )

    if action_type == "image":
        for each in actions:
            draw_image(*([canv, *each]))
    elif action_type == "text":
        for each in actions:
            draw_text(*([canv, *each]))

    canv.save()
    buff.seek(0)

    watermark = buff.read()
    buff.close()

    results = []

    for i in range(len(pdf_file.pages)):
        results.append(watermark if i == page_number - 1 else b"")

    return results


def merge_watermarks_with_pdf(
    pdf: bytes,
    watermarks: List[bytes],
) -> bytes:
    """Merges watermarks with PDF."""

    pdf_file = PdfReader(fdata=pdf)

    for i, page in enumerate(pdf_file.pages):
        if watermarks[i]:
            watermark = PdfReader(fdata=watermarks[i])
            if watermark.pages:
                merger = PageMerge(page)
                merger.add(watermark.pages[0]).render()

    return generate_stream(pdf_file)
