#!/usr/bin/env python

import os
import sys
import codecs
import warnings
import argparse

from enum import Enum
from pathlib import Path

from PIL import Image, ImageColor


# Declare constants
class TextAlign(Enum):
    FLUSH_LEFT = "left"
    CENTERED = "center"
    FLUSH_RIGHT = "right"

PATH = Path(__file__).parent.resolve()

DEFAULT_FONT_PATH = os.path.join(PATH, "Microfont_2D.png")
DEFAULT_ALIGN = TextAlign.FLUSH_LEFT
DEFAULT_BACKGROUND_COLOR = "#1a1a1e"
DEFAULT_TEXT_COLOR = "#f9f9f9"
DEFAULT_SPACING = 1
DEFAULT_PADDING = 8
DEFAULT_SCALE = 20


# Replaces all pixels in an Image with a specific color while still preserving transparency
def image_alpha_colorfill(image, color):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    r, g, b, a = image.split()
    
    color_image = Image.new("RGB", image.size, color)
    
    output_image = Image.new("RGBA", image.size)
    output_image.paste(color_image, (0, 0), mask=a)
    
    return output_image


# Renders text with an Image font into an output Image
def render_image_font(text,
                      font_image,
                      color=None,
                      align=TextAlign.FLUSH_LEFT,
                      scale=1,
                      spacing=1):
    function_name = sys._getframe().f_code.co_name
    if len(text) < 1:
        raise Exception(f"{function_name}() requires a non-zero length string as it's 'text'")
    if scale % 1 != 0:
        raise TypeError(f"{function_name}() requires an integer as a scaling factor (input 'scale': {scale})")
    if font_image.width % 16 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 16. (input 'font_image' width: {font_image.width})")
    if font_image.height % 8 != 0:
        raise Exception(f"{function_name}() requires a font image with a height divisible by 8. (input 'font_image' height: {font_image.height})")
    
    spacing = spacing * scale
    
    scaled_font_image = font_image.resize((font_image.width * scale, font_image.height * scale), resample=Image.Resampling.NEAREST)
    if color != None:  # Only change the color if it's specified
        font_image = image_alpha_colorfill(scaled_font_image, color)
    else:
        font_image = scaled_font_image
    
    char_width = font_image.width // 16
    char_height = font_image.height // 8
    
    text_width = 0
    text_height = 0
    for line in text.split("\n"):
        line_width = len(line)
        
        if line_width > text_width:
            text_width = line_width
        
        text_height += 1
    
    width = (char_width * text_width) + (spacing * (text_width-1))
    height = (char_height * text_height) + (spacing * (text_height-1))
    
    output_image = Image.new("RGBA", (width, height))
    
    for l, line in enumerate(text.split("\n")):
        line_width = (len(line) * (char_width + spacing)) - spacing
        line_blank_space = width - line_width
        
        x = 0
        y = l * (char_height + spacing)
        
        if align == TextAlign.FLUSH_RIGHT:
            x += line_blank_space
        elif align == TextAlign.CENTERED:
            x += line_blank_space // 2
        
        for c, char in enumerate(line):
            char_code = ord(char)
            if char_code not in range(0, 128):
                warnings.warn(f"character code \"{char_code}\" is not standard ASCII, replacing with a space")
                char_code = ord(" ")
            
            source_x = (char_code & 0b1111) * char_width
            source_y = (char_code >> 4) * char_height

            cut_box = (source_x, source_y, source_x + char_width, source_y + char_height)
            paste_position = (x, y)

            glyph_image = font_image.crop(cut_box)
            output_image.paste(glyph_image, paste_position)
            
            x += char_width + spacing
    
    return output_image


# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description=f"Renders text into an image using an image-based font.\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-t", "--text", dest="text", type=str, required=True,
                        help="the string to render"
                        )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=True,
                        help="the path and filename of the desired output image"
                        )
    
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=DEFAULT_FONT_PATH,
                        help=f"the path to the font image to use [\"{Path(DEFAULT_FONT_PATH).relative_to(PATH)}\"]"
                        )
    
    parser.add_argument("-c", "--color", dest="color", type=str, required=False, default=DEFAULT_TEXT_COLOR,
                        help=f"the color of the text [{DEFAULT_TEXT_COLOR}]"
                        )
    
    parser.add_argument("-b", "--background", dest="background", type=str, required=False, default=DEFAULT_BACKGROUND_COLOR,
                        help=f"the color of the background [{DEFAULT_BACKGROUND_COLOR}]"
                        )

    parser.add_argument("-a", "--align", dest="align", type=str, required=False, default=DEFAULT_ALIGN.value,
                        help=f"how to align the text {{{", ".join([x.value for x in TextAlign])}}} [{DEFAULT_ALIGN.value}]"
                        )
    
    parser.add_argument("-s", "--spacing", dest="spacing", type=int, required=False, default=DEFAULT_SPACING,
                        help=f"how many pixels to space the characters apart with [{DEFAULT_SPACING}]"
                        )
    
    parser.add_argument("-p", "--padding", dest="padding", type=int, required=False, default=DEFAULT_PADDING,
                        help=f"how many pixels to pad around the edges [{DEFAULT_PADDING}]"
                        )
    
    parser.add_argument("-x", "--scale", dest="scale", type=int, required=False, default=DEFAULT_SCALE,
                        help=f"how much to scale the final image by [{DEFAULT_SCALE}]"
                        )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    parsed_args.text = codecs.decode(parsed_args.text, "unicode_escape")
    
    parsed_args.output = Path(parsed_args.output)
    
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    parsed_args.color = ImageColor.getrgb(parsed_args.color)
    
    parsed_args.background = ImageColor.getrgb(parsed_args.background)
    
    if not parsed_args.align in [x.value for x in TextAlign]:
        parser.error(f"\"{parsed_args.align}\" is not a valid text alignment option")
    parsed_args.align = TextAlign(parsed_args.align)
    
    # Check integer arguments
    if parsed_args.spacing < 0:
        parser.error("spacing value cannot be negative")
    
    if parsed_args.padding < 0:
        parser.error("padding value cannot be negative")
    
    if parsed_args.scale < 1:
        parser.error("scale value cannot be less than 1")

    return parsed_args


def main(args):
    print()
    
    parsed_args = parse_args(args)
    
    text_image = render_image_font(
        text=parsed_args.text,
        font_image=parsed_args.font,
        color=parsed_args.color,
        align=parsed_args.align,
        scale=parsed_args.scale,
        spacing=parsed_args.spacing
    )
    
    padding = parsed_args.padding * parsed_args.scale
    output_size = (text_image.size[0] + (padding * 2), text_image.size[1] + (padding * 2))
    
    output_image = Image.new("RGBA", output_size, parsed_args.background + (255,))
    output_image.paste(text_image, (padding, padding), mask=text_image)
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
