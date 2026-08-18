import sys

from enum import Enum
from pathlib import Path

from PIL import Image, ImageColor

# Declare constants
class TextAlign(Enum):
    FLUSH_LEFT = "left"
    CENTERED = "center"
    FLUSH_RIGHT = "right"

PATH = Path(__file__).parent.parent.parent.resolve()

FONT_PATHS = {
    "1d": {
        "png": Path(PATH, "Microfont_1D.png"),
        "bmp": Path(PATH, "Microfont_1D.bmp")
    },
    "2d": {
        "png": Path(PATH, "Microfont_2D.png"),
        "bmp": Path(PATH, "Microfont_2D.bmp")
    },
}


# Replaces all pixels in an Image with a specific color while still preserving transparency
def image_alpha_colorfill(image, color):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    r, g, b, a = image.split()
    
    color_image = Image.new("RGB", image.size, color)
    
    output_image = Image.new("RGBA", image.size)
    output_image.paste(color_image, (0, 0), mask=a)
    
    return output_image


# Validates the size of a 1D Image font
def validate_image_font_1d(font_image, function_name):
    if font_image.width % 128 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 128. (input 'font_image' width: {font_image.width})")


# Returns the size of the characters in a 1D Image font
def image_font_char_size_1d(font_image):
    char_width = font_image.width // 128
    char_height = font_image.height
    
    return char_width, char_height


# Gets the glyph position for a character in a 1D Image font
def get_glyph_position_1d(char, char_size):
    char_code = ord(char)
    space_code = ord(" ")
    if char_code not in range(0, 128):
        warnings.warn(f"character \"{char}\" with code \"{char_code}\" is not standard ASCII, replacing with a space")
        char_code = space_code
    
    width, height = char_size
    
    x = char_code * width
    y = 0
    
    return x, y


# Validates the size of a 2D Image font
def validate_image_font_2d(font_image, function_name):
    if font_image.width % 16 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 16. (input 'font_image' width: {font_image.width})")
    if font_image.height % 8 != 0:
        raise Exception(f"{function_name}() requires a font image with a height divisible by 8. (input 'font_image' height: {font_image.height})")


# Returns the size of the characters in a 2D Image font
def image_font_char_size_2d(font_image):
    char_width = font_image.width // 16
    char_height = font_image.height // 8
    
    return char_width, char_height


# Gets the glyph position for a character in a 2D Image font
def get_glyph_position_2d(char, char_size):
    char_code = ord(char)
    if char_code not in range(0, 128):
        warnings.warn(f"character \"{char}\" with code \"{char_code}\" is not standard ASCII, replacing with a space")
        char_code = ord(" ")
    
    width, height = char_size
    
    x = (char_code & 0b1111) * width
    y = (char_code >> 4) * height
    
    return x, y


# Renders text with an Image font into an output Image
def render_image_font(text,
                      font_image,
                      validate_func,
                      size_func,
                      position_func,
                      color=None,
                      background=None,
                      padding=1,
                      align=TextAlign.FLUSH_LEFT,
                      scale=1,
                      spacing=1):
    function_name = sys._getframe().f_code.co_name
    if len(text) < 1:
        raise Exception(f"{function_name}() requires a non-zero length string as it's 'text'")
    if scale % 1 != 0:
        raise TypeError(f"{function_name}() requires an integer as a scaling factor (input 'scale': {scale})")
    validate_func(font_image, function_name)
    
    spacing = spacing * scale
    
    scaled_font_image = font_image.resize((font_image.width * scale, font_image.height * scale), resample=Image.Resampling.NEAREST)
    if color != None:  # Only change the color if it's specified
        font_image = image_alpha_colorfill(scaled_font_image, color)
    else:
        font_image = scaled_font_image
    
    char_width, char_height = size_func(font_image)
    
    text_width = 0
    text_height = 0
    for line in text.split("\n"):
        line_width = len(line)
        
        if line_width > text_width:
            text_width = line_width
        
        text_height += 1
    
    width = (char_width * text_width) + (spacing * (text_width-1))
    height = (char_height * text_height) + (spacing * (text_height-1))
    
    text_image = Image.new("RGBA", (width, height))
    
    for l, line in enumerate(text.split("\n")):
        line_width = (len(line) * (char_width + spacing)) - spacing
        line_blank_space = width - line_width
        
        x = 0
        y = l * (char_height + spacing)
        
        if align == TextAlign.FLUSH_RIGHT:
            x += line_blank_space
        elif align == TextAlign.CENTERED:
            x += line_blank_space // 2
        
        for c, char in enumerate(line):
            source_x, source_y = position_func(char, (char_width, char_height))

            cut_box = (source_x, source_y, source_x + char_width, source_y + char_height)
            paste_position = (x, y)

            glyph_image = font_image.crop(cut_box)
            text_image.paste(glyph_image, paste_position)
            
            x += char_width + spacing
    
    scaled_padding = padding * scale
    output_size = (text_image.size[0] + (scaled_padding * 2), text_image.size[1] + (scaled_padding * 2))
    
    if background == None:
        output_image = Image.new("RGBA", output_size, (0, 0, 0, 0))
    else:
        output_image = Image.new("RGBA", output_size, background + (255,))
    
    output_image.paste(text_image, (scaled_padding, scaled_padding), mask=text_image)
    
    return output_image


# Renders a 1D font Image font into a 2D font Image
def make_2d_font_from_1d_font(font_image):
    function_name = sys._getframe().f_code.co_name
    if font_image.width % 128 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 128. (input 'font_image' width: {font_image.width})")
    
    chars_wide = 16
    chars_tall = 8
    
    char_width = font_image.width // 128
    char_height = font_image.height
    
    row_width = char_width * chars_wide
    
    width = (char_width * chars_wide)
    height = (char_height * chars_tall)
    
    output_image = Image.new("RGBA", (width, height))
    
    for row in range(chars_tall):
        source_x = row * row_width
        cut_box = (source_x, 0, source_x + row_width, char_height)
        
        row_image = font_image.crop(cut_box)
        
        paste_x = 0
        paste_y = row * char_height
        paste_position = (paste_x, paste_y)
        
        output_image.paste(row_image, paste_position)
        
    return output_image


# Converts a transparent PNG font Image font into a black-and-white BMP font Image
# Just uses the alpha channel, ignores actual RGB color values
def make_bmp_from_png(font_image):
    output_image = Image.new("1", font_image.size, (0))
    
    foreground = Image.new("1", font_image.size, (1))
    
    output_image.paste(foreground, (0, 0), mask=font_image)
        
    return output_image


# Encodes a glyph 2D bitmap as a binary code
def encode_glyph_to_binary(g):
    flat = [x for xs in g for x in xs]
    sum = 0
    for i in range(len(flat)):
        sum += flat[i] << (14-i)
    
    return sum


# Decodes a binary code to a glyph 2D bitmap
def decode_glyph_from_binary(code, glyph_size):
    glyph = []
    for y in reversed(range(glyph_size[1])):
        row = []
        for x in reversed(range(glyph_size[0])):
            if code & (1 << ((glyph_size[0]*y)+x)) > 0:
                row.append(1)
            else:
                row.append(0)
        
        glyph.append(row)
    
    return glyph


# Converts each RGBA pixel of an Image into a 1 or 0 based on it's alpha channel
# Returns a 2D bitmap
def convert_alpha_to_bitmap(image, size):
    pixels = image.load()
    
    return [
        [1 if pixels[x,y][3] > 0 else 0 for y in range(size[1]) ] for x in range(size[0])
    ]


# Extracts a specific glyph from a 2D bitmap, as a 2D bitmap
def get_glyph_from_bitmap(bmp, i, glyph_size):
    return [
        [bmp[x][y] for x in range(glyph_size[0]*i, glyph_size[0]*(i+1))] for y in range(glyph_size[1])
    ]


# Automatically tests that the glyph encoder and decoder are working correctly
def test_binary_encoder_and_decoder(glyphs, glyph_size):
    code = [encode_glyph_to_binary(g) for g in glyphs]
    for i in range(len(code)):
        assert glyphs[i] == decode_glyph_from_binary(code[i], glyph_size), f"mismatch found on glyph {i}"


# Prints a 2D bitmap to the console
def print_bitmap(glyph):
    for row in glyph:
        for pixel in row:
            print("   " if pixel == 0 else "███", end="")
        print("")
    print("")


# Creates a string representing a table of binary codes from a list of glyph bitmaps
def create_binary_table_from_glyph_bitmaps(glyphs, indent=True):
    codes = [encode_glyph_to_binary(g) for g in glyphs]
    
    data = ["0x{:04x}".format(c) for c in codes]
    
    if indent:
        rows = [", ".join(data[(8*i)+j] for j in range(8)) for i in range(len(glyphs)//8)]
        data_string = ",\n    ".join(r for r in rows)
        
        return "{\n    " + data_string + "\n}"
    else:
        data_string = ", ".join(data)
        
        return "{" + data_string + "}"


# Creates a string representing a table of binary codes from a font Image
def create_binary_table_from_image(font_image, indent=True):
    function_name = sys._getframe().f_code.co_name
    if font_image.width % 128 != 0:
        raise Exception(f"{function_name}() requires a font image with a width divisible by 128. (input 'font_image' width: {font_image.width})")
    
    bitmap = convert_alpha_to_bitmap(font_image, font_image.size)
    
    glyph_size = (font_image.width // 128, font_image.height)
    glyphs = [get_glyph_from_bitmap(bitmap, i, glyph_size) for i in range(128)]
    
    test_binary_encoder_and_decoder(glyphs, glyph_size)
    
    return create_binary_table_from_glyph_bitmaps(glyphs, indent)
