from PIL import Image, ImageDraw, ImageFont
from bisect import bisect
import random

import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"

def convertToText(parameterImage):
    parameterImage = parameterImage.resize((int(parameterImage.size[0]*0.6), int(parameterImage.size[1]*0.45)))
    greyscaleLuminosities = [" ", " ", ".,-", "_ivc=!/|\\~", "gjez2]/(YL)t[+T7Vf",
                         "mdK4ZGbNDXY5P*Q", "W8KMA", "#%$"]

    zoneBoundaries = [36, 72, 108, 144, 180, 216, 252]

    finalString = ""
    for coordinateY in range(0, parameterImage.size[1]):
        for coordinateX in range(0,parameterImage.size[0]):
            luminosityValue = 255 - parameterImage.getpixel((coordinateX,
                                                    coordinateY))
            row = bisect(zoneBoundaries, luminosityValue)
            possibleLuminosityChoice = greyscaleLuminosities[row]
            finalString = finalString + possibleLuminosityChoice[random.randint(0, len(possibleLuminosityChoice) - 1)]
        finalString = finalString + "\n"

    return finalString

# coding=utf8

import PIL

def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 72  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image

def convertImageToImageText(image, index=""):
    openImage = image.resize((int(image.size[0]), int(image.size[1])), Image.BILINEAR)
    openImage = openImage.convert("L")

    imageText = convertToText(openImage)
    textFile = open("asciiArt.txt", "w")
    textFile.write(imageText)
    textFile.close()

    import webbrowser

    text_image("asciiArt.txt", font_path="Consolas.ttf").save("gif/" + index + "file.png")

openGif = Image.open("Moving-Car-Animation-Photoshop-PSD.gif")
x = 0
while True:
    convertImageToImageText(openGif, index=str(x))
    openGif.seek(openGif.tell() + 1)

    x += 1