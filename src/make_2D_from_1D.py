#!/usr/bin/env python

import os
import sys
import argparse

from pathlib import Path

from PIL import Image


# Declare constants
PATH = Path(__file__).parent.parent.resolve()

DEFAULT_FONT_IN_PATH = os.path.join(PATH, "microfont_1d.png")
DEFAULT_FONT_OUT_PATH = os.path.join(PATH, "microfont_2d.png")


# Renders a 1D font Image font into a 2D font Image
def make_2d_font_from_1d_font(font_image):
    function_name = sys._getframe().f_code.co_name
    if font_image.width % 128 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 128. (input 'font_image' width: {font_image.width})")
    
    chars_wide = 16
    chars_tall = 8
    
    char_width = font_image.width // 128
    char_height = font_image.height
    
    row_width = char_width * chars_wide
    
    width = (char_width * chars_wide)
    height = (char_height * chars_tall)
    
    output_image = Image.new("RGBA", (width, height))
    
    for row in range(chars_tall):
        source_x = row * row_width
        cut_box = (source_x, 0, source_x + row_width, char_height)
        
        row_image = font_image.crop(cut_box)
        
        paste_x = 0
        paste_y = row * char_height
        paste_position = (paste_x, paste_y)
        
        output_image.paste(row_image, paste_position)
        
    return output_image


# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description=f"Renders a 1D font Image font into a 2D font Image.\n"
                    f"Used to update the 2D sprite sheet automatically.\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=DEFAULT_FONT_IN_PATH,
                        help=f"the path to the 1D font image to use [\"{Path(DEFAULT_FONT_IN_PATH).relative_to(PATH)}\"]"
                        )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=False, default=DEFAULT_FONT_OUT_PATH,
                        help=f"the path and filename of the desired output 2D font image [{Path(DEFAULT_FONT_OUT_PATH).relative_to(PATH)}]"
                        )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    parsed_args.output = Path(parsed_args.output)

    return parsed_args


def main(args):
    print()
    parsed_args = parse_args(args)
    
    output_image = make_2d_font_from_1d_font(parsed_args.font)
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
