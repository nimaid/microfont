import codecs
import argparse

from pathlib import Path

from PIL import Image, ImageColor

from . import defaults, common


# Parse arguments for image generators
def parse_args_generate(args, default_font_path):
    parser = argparse.ArgumentParser(
        description=f"Renders text into an image using an image-based font.\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-t", "--text", dest="text", type=str, required=True,
                        help="the string to render"
                       )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=True,
                        help="the path and filename of the desired output image"
                       )
    
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=default_font_path,
                        help=f"the path to the font image to use [\"{Path(default_font_path).relative_to(common.PATH)}\"]"
                       )
    
    parser.add_argument("-c", "--color", dest="color", type=str, required=False, default=defaults.DEFAULT_TEXT_COLOR,
                        help=f"the color of the text [{defaults.DEFAULT_TEXT_COLOR}]"
                       )
    
    parser.add_argument("-b", "--background", dest="background", type=str, required=False, default=defaults.DEFAULT_BACKGROUND_COLOR,
                        help=f"the color of the background [{defaults.DEFAULT_BACKGROUND_COLOR}]"
                       )

    parser.add_argument("-a", "--align", dest="align", type=str, required=False, default=defaults.DEFAULT_ALIGN.value,
                        help=f"how to align the text {{{", ".join([x.value for x in common.TextAlign])}}} [{defaults.DEFAULT_ALIGN.value}]"
                       )
    
    parser.add_argument("-s", "--spacing", dest="spacing", type=int, required=False, default=defaults.DEFAULT_SPACING,
                        help=f"how many pixels to space the characters apart with [{defaults.DEFAULT_SPACING}]"
                       )
    
    parser.add_argument("-p", "--padding", dest="padding", type=int, required=False, default=defaults.DEFAULT_PADDING,
                        help=f"how many pixels to pad around the edges [{defaults.DEFAULT_PADDING}]"
                       )
    
    parser.add_argument("-x", "--scale", dest="scale", type=int, required=False, default=defaults.DEFAULT_SCALE,
                        help=f"how much to scale the final image by [{defaults.DEFAULT_SCALE}]"
                       )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    parsed_args.text = codecs.decode(parsed_args.text, "unicode_escape")
    
    parsed_args.output = Path(parsed_args.output)
    
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    parsed_args.color = ImageColor.getrgb(parsed_args.color)
    
    parsed_args.background = ImageColor.getrgb(parsed_args.background)
    
    if not parsed_args.align in [x.value for x in common.TextAlign]:
        parser.error(f"\"{parsed_args.align}\" is not a valid text alignment option")
    parsed_args.align = common.TextAlign(parsed_args.align)
    
    # Check integer arguments
    if parsed_args.spacing < 0:
        parser.error("spacing value cannot be negative")
    
    if parsed_args.padding < 0:
        parser.error("padding value cannot be negative")
    
    if parsed_args.scale < 1:
        parser.error("scale value cannot be less than 1")

    return parsed_args


# Parse arguments for converters
def parse_args_convert(args, default_font_in_path, default_font_out_path, description):
    parser = argparse.ArgumentParser(
        description=f"{description}\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=default_font_in_path,
                        help=f"the path to the 1D font image to use [\"{Path(default_font_in_path).relative_to(common.PATH)}\"]"
                       )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=False, default=default_font_out_path,
                        help=f"the path and filename of the desired output 2D font image [\"{Path(default_font_out_path).relative_to(common.PATH)}\"]"
                       )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    parsed_args.output = Path(parsed_args.output)

    return parsed_args


# Parse arguments for encoders
def parse_args_encode(args, default_font_path, description):
    parser = argparse.ArgumentParser(
        description=f"{description}\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=False, default=default_font_path,
                        help=f"the path to the 1D font image to use [\"{Path(default_font_path).relative_to(common.PATH)}\"]"
                        )
    parser.add_argument("-o", "--output", dest="output", type=str, required=False, default=None,
                        help="output file for the look-up table [None, print only]")
    parser.add_argument("-n", "--no_indent", dest="indent", action="store_false",
                        help="do not indent the output, write it all on one line")
    
    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = Image.open(font)
    
    if parsed_args.output is not None:
        parsed_args.output = Path(parsed_args.output)
    
    return parsed_args
