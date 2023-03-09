from PIL import Image, ImageDraw, ImageFont
import os
import countdown
from consts import *

EDITION_COLOUR = (100, 179, 232, 255)
DAYS_COLOUR = (128, 128, 128, 255)


def as1920(n):
    return n

def as800(n):
    return (n * 800) // 1920

def as400(n):
    return (n * 400) // 1920

def as200(n):
    return (n * 200) // 1920

def asSize(n, size):
    return (n * size) // 1920

sizes = [
    1920,
    800,
    400,
    200
]

def generate(edition, text, assets_path = "./assets/", generated_path = "./generated/"):

    os.makedirs(generated_path, exist_ok=True)

    for size in sizes:
        with Image.open(assets_path + BANNER_FILE_NAME + "_" + str(size) + ".png") as im:
            fnt1 = ImageFont.truetype(assets_path + FONT_ASSET, asSize(267, size))
            fnt2 = ImageFont.truetype(assets_path + FONT_ASSET, asSize(160, size))

            draw = ImageDraw.Draw(im)
            draw.fontmode = "L"

            draw.text((asSize(1200 - 3, size), asSize(340 - 5, size)), edition, font=fnt1, fill=EDITION_COLOUR, anchor="mm")
            draw.text((asSize(960 - 3, size), asSize(800 - 16, size)), text, font=fnt2, fill=DAYS_COLOUR, anchor="mm")

            im.save(generated_path + BANNER_FILE_NAME + "_" + str(size) + ".png")



if __name__ == "__main__":
    edit = countdown.load_edition("https://shadew.net/assets/nfcdata.json")
    generate(edit.name, edit.format_text())