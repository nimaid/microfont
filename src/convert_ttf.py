#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert_ttf(args, True,
                                             "Converts a TTF file to either a WOFF or WOFF2"
                                            )
    
    common.convert_ttf(parsed_args.font, parsed_args.output_format, output_path=parsed_args.output)
    print(f"Saved converted TTF to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
