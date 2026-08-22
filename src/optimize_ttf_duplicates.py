#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_convert_ttf(args, False,
                                             "Optimizes a TTF file by removing duplicate glyphs."
                                            )
    
    duplicates_removed = common.optimize_ttf_duplicates(parsed_args.font, parsed_args.output)
    print(f"Removed {duplicates_removed} duplicates, saved optimized TTF to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
