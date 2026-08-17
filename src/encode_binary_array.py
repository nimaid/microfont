#!/usr/bin/env python

import os
import sys
import argparse

from pathlib import Path

from PIL import Image

# Declare constants
PATH = Path(__file__).parent.parent.resolve()

DEFAULT_FONT_PATH = os.path.join(PATH, "Microfont_1D.png")


# Encodes a glyph 2D bitmap as a binary code
def encode_glyph(g):
    flat = [x for xs in g for x in xs]
    sum = 0
    for i in range(len(flat)):
        sum += flat[i] << (14-i)
    
    return sum


# Decodes a binary code to a glyph 2D bitmap
def decode_glyph(code, glyph_size):
    glyph = []
    for y in reversed(range(glyph_size[1])):
        row = []
        for x in reversed(range(glyph_size[0])):
            if code & (1 << ((glyph_size[0]*y)+x)) > 0:
                row.append(1)
            else:
                row.append(0)
        
        glyph.append(row)
    
    return glyph


# Converts each RGBA pixel of an Image into a 1 or 0 based on it's alpha channel
# Returns a 2D bitmap
def convert_to_bitmap(image, size):
    pixels = image.load()
    
    return [
        [1 if pixels[x,y][3] > 0 else 0 for y in range(size[1]) ] for x in range(size[0])
    ]


# Extracts a specific glyph from a 2D bitmap, as a 2D bitmap
def get_glyph(bmp, i, glyph_size):
    return [
        [bmp[x][y] for x in range(glyph_size[0]*i, glyph_size[0]*(i+1))] for y in range(glyph_size[1])
    ]


# Automatically tests that the glyph encoder and decoder are working correctly
def test_encoder_and_decoder(glyphs, glyph_size):
    code = [encode_glyph(g) for g in glyphs]
    for i in range(len(code)):
        assert glyphs[i] == decode_glyph(code[i], glyph_size), f"mismatch found on glyph {i}"


# Prints a 2D bitmap to the console
def print_bitmap(glyph):
    for row in glyph:
        for pixel in row:
            print("   " if pixel == 0 else "███", end="")
        print("")
    print("")


# Creates a string representing a table of binary codes from a list of glyphs
def create_table(glyphs, indent=True):
    codes = [encode_glyph(g) for g in glyphs]
    
    data = ["0x{:04x}".format(c) for c in codes]
    
    if indent:
        rows = [", ".join(data[(8*i)+j] for j in range(8)) for i in range(len(glyphs)//8)]
        data_string = ",\n    ".join(r for r in rows)
        
        return "{\n    " + data_string + "\n}"
    else:
        data_string = ", ".join(data)
        
        return "{" + data_string + "}"


# Creates a string representing a table of binary codes from a font Image
def create_table_from_image(font_image, indent=True):
    function_name = sys._getframe().f_code.co_name
    if font_image.width % 128 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 128. (input 'font_image' width: {font_image.width})")
    
    bitmap = convert_to_bitmap(font_image, font_image.size)
    
    glyph_size = (font_image.width // 128, font_image.height)
    glyphs = [get_glyph(bitmap, i, glyph_size) for i in range(128)]
    
    test_encoder_and_decoder(glyphs, glyph_size)
    
    return create_table(glyphs, indent)


# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description=f"Encodes each character as an unsigned 16-bit integer.\n"
                    f"Generates a look-up table that can be simply pasted into source code.\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=DEFAULT_FONT_PATH,
                        help=f"the path to the 1D font image to use [\"{Path(DEFAULT_FONT_PATH).relative_to(PATH)}\"]"
                        )
    parser.add_argument("-o", "--output", dest="output", type=str, required=False, default=None,
                        help="output file for the look-up table [None, print only]")
    parser.add_argument("-n", "--no_indent", dest="indent", action="store_false",
                        help="do not indent the output, write it all on one line")
    
    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    if parsed_args.output is not None:
        parsed_args.output = Path(parsed_args.output)
    
    return parsed_args


def main(args):
    parsed_args = parse_args(args)
    
    output = create_table_from_image(parsed_args.font, parsed_args.indent)
    
    if parsed_args.output is None:
        print(output)
    else:
        with open(parsed_args.output, "w") as file_out:
            file_out.write(output)


if __name__ == "__main__":
    main(sys.argv[1:])
