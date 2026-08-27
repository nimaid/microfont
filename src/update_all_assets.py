#!/usr/bin/env python

import sys

from pathlib import Path

from PIL import Image, ImageColor, ImageFont

from modules import common, defaults

def main(args):
    print()
    
    # Optimize proportional .ttf
    proportional_duplicates = common.optimize_ttf_duplicates(common.FONT_PATHS["raw_ttf"]["proportional"], common.FONT_PATHS["optimized_raw_ttf"]["proportional"])
    # Update manufacturer
    common.update_ttf_manufacturer(common.FONT_PATHS["optimized_raw_ttf"]["proportional"], common.FONT_PATHS["manufacturer_raw_ttf"]["proportional"])
    # Update copyright year
    common.update_pixelforge_ttf_copyright_year(common.FONT_PATHS["manufacturer_raw_ttf"]["proportional"], common.FONT_PATHS["ttf"]["proportional"])
    print(f"Updated proportional TTF (removed {proportional_duplicates} duplicate glyphs)")
    
    # Convert proportional .ttf to .woff
    common.convert_ttf(common.FONT_PATHS["ttf"]["proportional"], common.FontFormats.WOFF)
    print("Updated proportional WOFF")
    
    # Convert proportional .ttf to .woff2
    common.convert_ttf(common.FONT_PATHS["ttf"]["proportional"], common.FontFormats.WOFF2)
    print("Updated proportional WOFF2")
    
    # Optimize monospaced .ttf
    monospaced_duplicates = common.optimize_ttf_duplicates(common.FONT_PATHS["raw_ttf"]["monospaced"], common.FONT_PATHS["optimized_raw_ttf"]["monospaced"])
    # Update manufacturer
    common.update_ttf_manufacturer(common.FONT_PATHS["optimized_raw_ttf"]["monospaced"], common.FONT_PATHS["manufacturer_raw_ttf"]["monospaced"])
    # Update copyright year
    common.update_pixelforge_ttf_copyright_year(common.FONT_PATHS["manufacturer_raw_ttf"]["monospaced"], common.FONT_PATHS["ttf"]["monospaced"])
    print(f"Updated monospaced TTF (removed {monospaced_duplicates} duplicate glyphs)")
    
    # Convert monospaced .ttf to .woff
    common.convert_ttf(common.FONT_PATHS["ttf"]["monospaced"], common.FontFormats.WOFF)
    print("Updated monospaced WOFF")
    
    # Convert monospaced .ttf to .woff2
    common.convert_ttf(common.FONT_PATHS["ttf"]["monospaced"], common.FontFormats.WOFF2)
    print("Updated monospaced WOFF2\n")
    
    # Make 1D PNG from monospaced TTF
    font_monospaced = common.open_ttf_at_dpi(common.FONT_PATHS["ttf"]["monospaced"], common.FONT_SIZE, common.FONT_DPI)
    font_image_1d_png = common.create_1d_font_from_ttf(font_monospaced, common.FONT_CHAR_SIZE, char_line_spacing=common.FONT_CHAR_LINE_SPACING)
    font_image_1d_png.save(common.FONT_PATHS["1d"]["png"])
    print("Updated 1D PNG")
    
    # Make 2D PNG from 1D PNG
    font_image_2d_png = common.make_2d_font_from_1d_font(font_image_1d_png)
    font_image_2d_png.save(common.FONT_PATHS["2d"]["png"])
    print("Updated 2D PNG")
    
    # Make 1D BMP from 1D PNG
    common.make_bmp_from_png(font_image_1d_png).save(common.FONT_PATHS["1d"]["bmp"])
    print("Updated 1D BMP")
    
    # Make 2D BMP from 2D PNG
    common.make_bmp_from_png(font_image_2d_png).save(common.FONT_PATHS["2d"]["bmp"])
    print("Updated 2D BMP\n")
    
    # Make temp folder
    temp_folder = Path(common.PATH, "temp")
    temp_folder.mkdir(parents=True, exist_ok=True)
    
    # Render demo image
    default_text_color = ImageColor.getrgb(defaults.DEFAULT_TEXT_COLOR)
    default_background_color = ImageColor.getrgb(defaults.DEFAULT_BACKGROUND_COLOR)
    base_image = common.render_image_font(
        text="3x5 Microfont by\nElla Jameson (nimaid)\n\nABCDEFGHIJKLM\nabcdefghijklm\n\nNOPQRSTUVWXYZ\nnopqrstuvwxyz\n\n`1234567890-=[]\\;',./\n~!@#$%^&*()_+{}|:\"<>?",
        font_image=font_image_1d_png,
        validate_func=common.validate_image_font_1d,
        size_func=common.image_font_char_size_1d,
        position_func=common.get_glyph_position_1d,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.CENTERED,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    )
    
    logo_text = "   by __      __\n     /  \\    /  \\\n    / /\\ \\  / /\\ \\\n   /  \\X\\ \\ \\ \\X\\ \\\n  / /\\ \\X\\ \\ \\ \\X\\ \\\n / /X/  \\X\\ \\ \\ \\X\\ \\\n/ /X/ /\\ \\X\\ \\ \\ \\X\\ \\\n\\ \\X\\ \\ \\ \\X\\ \\/ /X/ /\n \\ \\X\\ \\ \\ \\X\\  /X/ /\n  \\ \\X\\ \\ \\ \\X\\ \\/ /\n   \\ \\X\\ \\ \\ \\X\\  /\n    \\ \\/ /  \\ \\/ /\n     \\__/    \\__/imaid"
    logo_image = common.render_image_font(
        text=logo_text,
        font_image=font_image_1d_png,
        validate_func=common.validate_image_font_1d,
        size_func=common.image_font_char_size_1d,
        position_func=common.get_glyph_position_1d,
        color=default_text_color,
        background=None,
        padding=0,
        align=common.TextAlign.FLUSH_LEFT,
        scale=1,
        spacing=defaults.DEFAULT_SPACING
    )
    
    logo_padding = 32
    x = (base_image.width - logo_image.width) - logo_padding
    y = (base_image.height - logo_image.height) - logo_padding
    base_image.paste(logo_image, (x, y), mask=logo_image)
    
    base_image.save(Path(common.PATH, "docs", "demo.png"))
    base_image.convert("RGB").save(Path(temp_folder, "demo.jpg"))
    print("Updated demo image")
    
    # Render pangram image
    font_proportional = common.open_ttf_at_dpi(common.FONT_PATHS["ttf"]["proportional"], common.FONT_SIZE, common.FONT_DPI)
    common.render_ttf_font(
        text="Angry Buzzing Citizens\nDenounced Equine Federal\nGovernment Hijackers In July,\nKeeping Local Militias\nNear Our Public Quarters,\nRapidly Silencing Toxic\nUnderworld Violence Without\nXenografting Young Zebras.",
        font=font_proportional,
        char_size=common.FONT_CHAR_SIZE,
        char_line_spacing=common.FONT_CHAR_LINE_SPACING,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.CENTERED,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    ).save(Path(common.PATH, "docs", "pangram.png"))
    print("Updated pangram image")
    
    # Render Spanish image
    common.render_ttf_font(
        text="El veloz murciélago\nhindú comía feliz\ncardillo y kiwi.\nLa cigüeña tocaba\nel saxofón detrás\ndel palenque de paja.",
        font=font_proportional,
        char_size=common.FONT_CHAR_SIZE,
        char_line_spacing=common.FONT_CHAR_LINE_SPACING,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.CENTERED,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    ).save(Path(common.PATH, "docs", "spanish.png"))
    print("Updated Spanish image")
    
    # Render Greek image
    common.render_ttf_font(
        text="Ταχίστη αλώπηξ βαφής\nψημένη γη, δρασκελίζει\nυπέρ νωθρού κυνός\nTakhístè alôpèx vaphês\npsèménè gè, draskelízei\nypér nòthroý kynós",
        font=font_proportional,
        char_size=common.FONT_CHAR_SIZE,
        char_line_spacing=common.FONT_CHAR_LINE_SPACING,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.CENTERED,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    ).save(Path(common.PATH, "docs", "greek.png"))
    print("Updated Greek image")
    
    # Render poem image
    poem_image = common.render_ttf_font(
        text="I met a traveller from an antique land\nWho said: Two vast and trunkless legs of stone\nStand in the desert. Near them, on the sand,\nHalf sunk, a shattered visage lies, whose frown,\nAnd wrinkled lip, and sneer of cold command,\nTell that its sculptor well those passions read\nWhich yet survive, stamped on these lifeless things,\nThe hand that mocked them and the heart that fed:\nAnd on the pedestal these words appear:\n\"My name is Ozymandias, king of kings:\nLook on my works, ye Mighty, and despair!\"\nNothing beside remains. Round the decay\nOf that colossal wreck, boundless and bare\nThe lone and level sands stretch far away.",
        font=font_proportional,
        char_size=common.FONT_CHAR_SIZE,
        char_line_spacing=common.FONT_CHAR_LINE_SPACING,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.FLUSH_LEFT,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    )
    poem_image.save(Path(common.PATH, "docs", "poem.png"))
    print("Updated poem image")
    
    # Render poem image (Itch.io)
    poem_image.resize(tuple((x * 17) // defaults.DEFAULT_SCALE for x in poem_image.size), resample=Image.Resampling.NEAREST).save(Path(temp_folder, "poem.png"))
    print("Updated poem image (Itch.io)")
    
    # Render code image
    common.render_image_font(
        text="#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    \n    return 0;\n}",
        font_image=font_image_1d_png,
        validate_func=common.validate_image_font_1d,
        size_func=common.image_font_char_size_1d,
        position_func=common.get_glyph_position_1d,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.FLUSH_LEFT,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    ).save(Path(common.PATH, "docs", "code.png"))
    print("Updated code image")
    
    # Render road image
    road_image = common.render_ttf_font(
        text="Two roads diverged in a yellow wood,\nAnd sorry I could not travel both\nAnd be one traveler, long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth;\n\nThen took the other, as just as fair,\nAnd having perhaps the better claim,\nBecause it was grassy and wanted wear;\nThough as for that the passing there\nHad worn them really about the same,\n\nAnd both that morning equally lay\nIn leaves no step had trodden black.\nOh, I kept the first for another day!\nYet knowing how way leads on to way,\nI doubted if I should ever come back.\n\nI shall be telling this with a sigh\nSomewhere ages and ages hence:\nTwo roads diverged in a wood, and I-\nI took the one less traveled by,\nAnd that has made all the difference.",
        font=font_proportional,
        char_size=common.FONT_CHAR_SIZE,
        char_line_spacing=common.FONT_CHAR_LINE_SPACING,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.FLUSH_LEFT,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    )
    road_image.save(Path(common.PATH, "docs", "road.png"))
    print("Updated road image")
    
    # Render road image (Itch.io)
    road_image.resize(tuple((x * 14) // defaults.DEFAULT_SCALE for x in road_image.size), resample=Image.Resampling.NEAREST).save(Path(temp_folder, "road.png"))
    print("Updated road image (Itch.io)")
    
    # Render logo image
    common.render_image_font(
        text=logo_text,
        font_image=font_image_1d_png,
        validate_func=common.validate_image_font_1d,
        size_func=common.image_font_char_size_1d,
        position_func=common.get_glyph_position_1d,
        color=default_text_color,
        background=default_background_color,
        padding=defaults.DEFAULT_PADDING,
        align=common.TextAlign.FLUSH_LEFT,
        scale=defaults.DEFAULT_SCALE,
        spacing=defaults.DEFAULT_SPACING
    ).save(Path(common.PATH, "docs", "logo.png"))
    print("Updated logo image\n")
    
    # Replace binary array in main readme
    readme_path = Path(common.PATH, "README.md")
    with open(readme_path, "r") as f:
        readme = f.read()
    
    binary_array_pre = "Here is that array for the current iteration of the Microfont:\n```\n"
    binary_array_post = "\n```\n\n<br />\n<details>\n\n<summary>How To Use The Binary Array</summary>"
    
    binary_array_start = readme.find(binary_array_pre)
    if binary_array_start == -1:
        raise Exception("Could not find binary array pre-string")
    else:
        binary_array_start += len(binary_array_pre)
    
    binary_array_end = readme.find(binary_array_post)
    if binary_array_end == -1:
        raise Exception("Could not find binary array post-string")
    
    binary_array = common.create_binary_table_from_image(font_image_1d_png)
    
    readme = readme[:binary_array_start] + binary_array + readme[binary_array_end:]
    
    with open(readme_path, "w", newline='\n') as f:
        f.write(readme)
    
    print("Updated readme")


if __name__ == "__main__":
    main(sys.argv[1:])
