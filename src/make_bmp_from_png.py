#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert(args, common.FONT_PATHS["1d"]["png"], common.FONT_PATHS["1d"]["bmp"],
                                             "Converts a transparent PNG font image into a black-and-white BMP font image.\n"
                                             "Used to update the BMP sprite sheets automatically."
                                            )
    
    output_image = common.make_bmp_from_png(parsed_args.font)
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
