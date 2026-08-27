#!/usr/bin/env python

import sys

from modules import common, defaults, parsers


def main(args):
    print()
    parsed_args = parsers.parse_args_proportional(
        args=args,
        default_font_path=common.FONT_PATHS["ttf"]["proportional"],
        default_font_size=common.FONT_SIZE,
        default_font_dpi=common.FONT_DPI,
        default_font_char_width=common.FONT_CHAR_SIZE[0],
        default_font_char_height=common.FONT_CHAR_SIZE[1],
        default_font_char_line_spacing=common.FONT_CHAR_LINE_SPACING
    )
    
    output_image = common.render_ttf_font(
        text=parsed_args.text,
        font=parsed_args.font,
        char_size=parsed_args.font_char_size,
        char_line_spacing=parsed_args.font_char_line_spacing,
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
