#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert_ttf(args, False,
                                             "Updates the copyright year of a TTF file exported from PixelForge."
                                            )
    
    common.update_pixelforge_ttf_copyright_year(parsed_args.font, parsed_args.output)
    print(f"Saved updated TTF to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
