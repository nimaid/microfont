#!/usr/bin/env python

import sys
import argparse
from PIL import Image

# glyph width and height
w, h = 3, 5

def parse_args(args):
    parser = argparse.ArgumentParser(
        description=
            '''
            Encodes each character as an unsigned 16-bit integer.
            Generates a look-up table that can be simply pasted into source code.
            '''
    )
    parser.add_argument("-i", "--input", dest="fname", default="microfont_1d.png",
                        help="Path and filename to the 1D spritesheet file.")
    parser.add_argument("-o", "--output", dest="out", default=None,
                        help="Output file for the look-up table.")
    parser.add_argument("-n", "--noindent", dest="noindent", action="store_true",
                        help="Do NOT indent the output, write it all on one line.")
    return parser.parse_args()

def convert_to_bitmap(pixels, size):
    return [
        [1 if pixels[x,y][3] > 0 else 0 for y in range(size[1]) ] for x in range(size[0])
    ]

def get_glyph(bmp, i):
    return [
        [bmp[x][y] for x in range(w*i, w*(i+1))] for y in range(5)
    ]

def encode_glyph(g):
    flat = [x for xs in g for x in xs]
    sum = 0
    for i in range(len(flat)):
        sum += flat[i] * (2**(14-i))
    return sum

def decode_glyph(code):
    glyph = [
        [ 1 if code & (1<<(w*y+x)) else 0 for x in reversed(range(w)) ] for y in reversed(range(h))
    ]
    return glyph

def test_encoder_and_decoder(glyphs):
    code = [encode_glyph(g) for g in glyphs]
    for i in range(len(code)):
        assert glyphs[i] == decode_glyph(code[i]), f"mismatch found on glyph {i}"

def print_glyph(glyph):
    for y in range(h):
        for x in range(w):
            print('   ' if glyph[y][x] == 0 else '███', end='')
        print('')
    print('')

def create_table(glyphs, noindent=False):
    codes = [encode_glyph(g) for g in glyphs]
    data = ['0x{:04x}'.format(c) for c in codes]
    if noindent is True:
        return '{' + ', '.join(data) + '}'
    else:
        rows = [', '.join(data[8*i+j] for j in range(8)) for i in range(len(glyphs)//8)]
        data = ',\n    '.join(r for r in rows)
        return '{\n    ' + data + '\n}'

def main(args):
    args = parse_args(args)
    file_in = Image.open(args.fname)
    bitmap = convert_to_bitmap(file_in.load(), file_in.size)
    glyphs = [get_glyph(bitmap, i) for i in range(128)]
    test_encoder_and_decoder(glyphs)
    output = create_table(glyphs, args.noindent)
    if args.out is None:
        print(output)
    else:
        with open(args.out, "w") as file_out:
            file_out.write(output)

if __name__ == "__main__":
    main(sys.argv)