import codecs
import argparse

from pathlib import Path

from PIL import Image, ImageColor, ImageFont

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
                        help=f"the color of the text {{\"#rrggbb\"}} [\"{defaults.DEFAULT_TEXT_COLOR}\"]"
                       )
    
    parser.add_argument("-b", "--background", dest="background", type=str, required=False, default=defaults.DEFAULT_BACKGROUND_COLOR,
                        help=f"the color of the background {{\"#rrggbb\", \"None\"}} [\"{defaults.DEFAULT_BACKGROUND_COLOR}\"]"
                       )

    parser.add_argument("-a", "--align", dest="align", type=str, required=False, default=defaults.DEFAULT_ALIGN.value,
                        help=f"how to align the text {{{"\"" + "\", \"".join([x.value for x in common.TextAlign]) + "\""}}} [\"{defaults.DEFAULT_ALIGN.value}\"]"
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
    
    if parsed_args.background.lower().strip() == "none":
        parsed_args.background = parsed_args.color[:3] + (0, )
    else:
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

# Parse arguments for proportional image generator
def parse_args_proportional(args, default_font_path, default_font_size, default_font_char_width, default_font_char_height, default_font_char_line_spacing):
    parser = argparse.ArgumentParser(
        description=f"Renders text into an image using the proportional TTF font.\n\n"
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
                        help=f"the path to the font TTF to use [\"{Path(default_font_path).relative_to(common.PATH)}\"]"
                       )
                       
    parser.add_argument("-fs", "--font_size", dest="font_size", type=int, required=False, default=default_font_size,
                        help=f"the size at which the font renders pixel-perfect at 1x [{default_font_size}]"
                       )
    
    parser.add_argument("-fw", "--font_char_width", dest="font_char_width", type=int, required=False, default=default_font_char_width,
                        help=f"how many pixels tall each character is [{default_font_char_width}]"
                       )
                       
    parser.add_argument("-fh", "--font_char_height", dest="font_char_height", type=int, required=False, default=default_font_char_height,
                        help=f"how many pixels tall each character is [{default_font_char_height}]"
                       )
    
    parser.add_argument("-fl", "--font_char_line_spacing", dest="font_char_line_spacing", type=int, required=False, default=default_font_char_line_spacing,
                        help=f"how many pixels to space the lines apart with [{default_font_char_line_spacing}]"
                       )
    
    parser.add_argument("-c", "--color", dest="color", type=str, required=False, default=defaults.DEFAULT_TEXT_COLOR,
                        help=f"the color of the text {{\"#rrggbb\"}} [\"{defaults.DEFAULT_TEXT_COLOR}\"]"
                       )
    
    parser.add_argument("-b", "--background", dest="background", type=str, required=False, default=defaults.DEFAULT_BACKGROUND_COLOR,
                        help=f"the color of the background {{\"#rrggbb\", \"None\"}} [\"{defaults.DEFAULT_BACKGROUND_COLOR}\"]"
                       )

    parser.add_argument("-a", "--align", dest="align", type=str, required=False, default=defaults.DEFAULT_ALIGN.value,
                        help=f"how to align the text {{{"\"" + "\", \"".join([x.value for x in common.TextAlign]) + "\""}}} [\"{defaults.DEFAULT_ALIGN.value}\"]"
                       )
    
    parser.add_argument("-s", "--spacing", dest="spacing", type=int, required=False, default=defaults.DEFAULT_SPACING,
                        help=f"how many pixels to space the lines apart with [{defaults.DEFAULT_SPACING}]"
                       )
    
    parser.add_argument("-p", "--padding", dest="padding", type=int, required=False, default=defaults.DEFAULT_PADDING,
                        help=f"how many pixels to pad around the edges [{defaults.DEFAULT_PADDING}]"
                       )
    
    parser.add_argument("-x", "--scale", dest="scale", type=int, required=False, default=defaults.DEFAULT_SCALE,
                        help=f"how much to scale the final image by [{defaults.DEFAULT_SCALE}]"
                       )

    parsed_args = parser.parse_args(args)
    
    # Check integer arguments
    if parsed_args.font_size < 1:
        parser.error("font_size value cannot be less than 1")
    
    if parsed_args.font_char_width < 1:
        parser.error("font_char_width value cannot be less than 1")
    
    if parsed_args.font_char_height < 1:
        parser.error("font_char_height value cannot be less than 1")
    
    parsed_args.font_char_size = (parsed_args.font_char_width, parsed_args.font_char_height)
    
    if parsed_args.font_char_line_spacing < 0:
        parser.error("font_char_line_spacing value cannot be negative")
    
    if parsed_args.spacing < 0:
        parser.error("spacing value cannot be negative")
    
    if parsed_args.padding < 0:
        parser.error("padding value cannot be negative")
    
    if parsed_args.scale < 1:
        parser.error("scale value cannot be less than 1")
    
    # Interpret string arguments
    parsed_args.text = codecs.decode(parsed_args.text, "unicode_escape")
    
    parsed_args.output = Path(parsed_args.output)
    
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    if font.suffix.lower() != ".ttf":
        parser.error(f"the file \"{font}\" is not a valid TTF file")
    parsed_args.font = ImageFont.truetype(font, parsed_args.font_size)
    
    parsed_args.color = ImageColor.getrgb(parsed_args.color)
    
    if parsed_args.background.lower().strip() == "none":
        parsed_args.background = parsed_args.color[:3] + (0, )
    else:
        parsed_args.background = ImageColor.getrgb(parsed_args.background)
    
    if not parsed_args.align in [x.value for x in common.TextAlign]:
        parser.error(f"\"{parsed_args.align}\" is not a valid text alignment option")
    parsed_args.align = common.TextAlign(parsed_args.align)
    
    

    return parsed_args


# Parse arguments for image converters
def parse_args_convert_image(args, default_font_in_path, default_font_out_path, description):
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


# Parse arguments for TTF converters
def parse_args_convert_ttf(args, get_output_format, description):
    parser = argparse.ArgumentParser(
        description=f"{description}\n\n"
                    f"Valid parameters are shown in {{braces}}.\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--font", dest="font", type=str, required=True,
                        help=f"the path to the TTF to convert"
                       )
    
    parser.add_argument("-o", "--output", dest="output", type=str, required=True,
                        help=f"the path and filename of the desired output font file"
                       )

    parsed_args = parser.parse_args(args)
    
    # Interpret string arguments
    font = Path(parsed_args.font)
    if not font.is_file():
        parser.error(f"the file \"{font}\" does not exist")
    parsed_args.font = font
    
    output = Path(parsed_args.output)
    if font.resolve(strict=False) == output.resolve(strict=False):
        parser.error("the output font file must be different than the input one")
    parsed_args.output = output
    
    if get_output_format:
        extension = parsed_args.output.suffix.lower()
        valid_extensions = [("." + x.value) for x in common.FontFormats]
        if extension not in valid_extensions:
            parser.error(f"the output extension \"{extension}\" is not valid. Options: \"" + "\", \"".join(valid_extensions) + "\"")
        parsed_args.output_format = common.FontFormats(extension.strip("."))
    
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
