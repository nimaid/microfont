#!/usr/bin/env python

import sys

from modules import common, defaults, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_generate(args, common.FONT_PATHS["2d"]["png"])
    
    output_image = common.render_image_font(
        text=parsed_args.text,
        font_image=parsed_args.font,
        validate_func=common.validate_image_font_2d,
        size_func=common.image_font_char_size_2d,
        position_func=common.get_glyph_position_2d,
        color=parsed_args.color,
        background=parsed_args.background,
        padding=parsed_args.padding,
        align=parsed_args.align,
        scale=parsed_args.scale,
        spacing=parsed_args.spacing
    )
    
    if parsed_args.output.suffix.lower() in common.RGB_ONLY_FORMATS:
        output_image = output_image.convert("RGB")
    
    output_image.save(parsed_args.output)
    print(f"Saved image to \"{parsed_args.output}\"")


if __name__ == "__main__":
    main(sys.argv[1:])
