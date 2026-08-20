#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert_ttf(args, False,
                                             "Fixes the Units Per Em (UPEM) value of a TTF file exported from PixelForge to make the suggested font sizes accurate.\n"
                                             "Basically, there is a bug in PixelForge that makes the UPEM 133.33% larger than it should be.\n"
                                             "This simply scales the UPEM down by 75%."
                                            )
    
    common.fix_pixelforge_ttf_scaling(parsed_args.font, parsed_args.output)
    print(f"Saved fixed TTF to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
