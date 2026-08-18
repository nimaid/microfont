#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert(args, common.FONT_PATHS["1d"]["png"], common.FONT_PATHS["2d"]["png"],
                                             "Renders a 1D font image into a 2D font Image.\n"
                                             "Used to update the 2D sprite sheets automatically."
                                            )
    
    output_image = common.make_2d_font_from_1d_font(parsed_args.font)
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
