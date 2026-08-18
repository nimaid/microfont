#!/usr/bin/env python

import sys

from modules import common, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_encode(args, common.FONT_PATHS["1d"]["png"],
                             "Encodes each character as an unsigned 16-bit integer.\n"
                             "Generates a look-up table that can be simply pasted into source code."
                            )
    
    output = common.create_binary_table_from_image(parsed_args.font, parsed_args.indent)
    
    if parsed_args.output is None:
        print(output)
    else:
        with open(parsed_args.output, "w") as file_out:
            file_out.write(output)
        print(f"Saved array to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
