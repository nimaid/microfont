#!/usr/bin/env python

import os
import sys
import argparse

from pathlib import Path

from PIL import Image


# Declare constants
PATH = Path(__file__).parent.parent.resolve()

DEFAULT_FONT_IN_PATH = os.path.join(PATH, "Microfont_1D.png")
DEFAULT_FONT_OUT_PATH = os.path.join(PATH, "Microfont_1D.bmp")


# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description=f"Converts a transparent PNG font image into a black-and-white BMP font image.\n"
                    f"Used to update the BMP sprite sheets automatically.\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=DEFAULT_FONT_IN_PATH,
                        help=f"the path to the 1D font image to use [\"{Path(DEFAULT_FONT_IN_PATH).relative_to(PATH)}\"]"
                        )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=False, default=DEFAULT_FONT_OUT_PATH,
                        help=f"the path and filename of the desired output 2D font image [\"{Path(DEFAULT_FONT_OUT_PATH).relative_to(PATH)}\"]"
                        )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    parsed_args.output = Path(parsed_args.output)

    return parsed_args


# Converts a transparent PNG font Image font into a black-and-white BMP font Image
# Just uses the alpha channel, ignores actual RGB color values
def make_bmp_from_png(font_image):
    output_image = Image.new("1", font_image.size, (0))
    
    foreground = Image.new("1", font_image.size, (1))
    
    output_image.paste(foreground, (0, 0), mask=font_image)
        
    return output_image


def main(args):
    print()
    parsed_args = parse_args(args)
    
    output_image = make_bmp_from_png(parsed_args.font)
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
