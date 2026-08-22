#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_replace_ttf_field(args,
                                             "Updates the manufacturer field of a TTF file."
                                            )
    
    common.update_ttf_manufacturer(parsed_args.font, parsed_args.output, manufacturer=parsed_args.text)
    print(f"Saved updated TTF to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
