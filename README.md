# 3x5 Microfont
A Highly Legible 3x5 Pixel Font With Full ASCII Support

<p align="center"><img src="docs/demo.png" width="400px" alt="A demo of every ASCII character."/></p>

## Examples

<p align="center"><img src="docs/pangram.png" width="400px" alt="The classic pangram about a quick brown fox."/></p>

<p align="center"><img src="docs/poem.png" width="400px" alt="The poem &quot;Ozymandias&quot; by Percy Bysshe Shelley."/></p>

<p align="center"><img src="docs/code.png" width="400px" alt="A standard &quot;Hello, World!&quot; program written in C."/></p>

<p align="center"><img src="docs/road.png" width="400px" alt="The poem &quot;The Road Not Taken&quot; by Robert Frost."/></p>

<p align="center"><img src="docs/logo.png" width="400px" alt="ASCII art of my logo."/></p>

## Calculating Glyph Position
The layout of the images has been optimized to make converting from an ASCII character code to X and Y coordinates extremely simple.

All characters are `3` pixels wide by `5` pixels tall. The X and Y coordinates calculated below are for the **top left corner** of the desired glyph. So the full bounding box for any glyph is:
```
left = x
right = x + 3
top = y
bottom = y + 5
```

### 1D Calculations
These calculations work for [`Microfont_1D.png`](https://raw.githubusercontent.com/nimaid/microfont/refs/heads/main/Microfont_1D.png) and are probably the simplest to do. The X coordinate is directly related to the full ASCII character code.

```
x = get_ascii_code(character) * 3
y = 0
```

### 2D Calculations
These calculations work for [`Microfont_2D.png`](https://raw.githubusercontent.com/nimaid/microfont/refs/heads/main/Microfont_2D.png). While they are slightly more complex, they allow for the source image to be a more reasonable aspect ratio. The X coordinate is based on the low nibble of the character code and the Y coordinate is based on the high nibble.

```
x = (get_ascii_code(character) & 0b1111) * 3
y = (get_ascii_code(character) >> 4) * 5
```

## Example Code: Image Generators
I have included two Python scripts named `generate_1d.py` and `generate_2d.py`. Both are tools with a command line interface that render text into images using a font image.

However:
- `generate_1d.py` demonstrates how to use `Microfont_1D.png`
- `generate_2d.py` demonstrates how to use `Microfont_2D.png`

To use the scripts, you need to install `Pillow`:
```
pip install Pillow
```

Then you can see how to use the scripts with:
```
python generate_1d.py --help
python generate_2d.py --help
```

## TrueType Fonts
Thanks to the freeware program [PixelForge](https://www.pixel-forge.com/), I was also able to create `.ttf` versions of this font!
- The [`Microfont-Mono.ttf`](https://raw.githubusercontent.com/nimaid/microfont/refs/heads/main/Microfont-Mono.ttf) file is a truly faithful recreation of the monospaced results you would normally get using this font programmatically from the sprite sheet.
- The [`Microfont.ttf`](https://raw.githubusercontent.com/nimaid/microfont/refs/heads/main/Microfont.ttf) file is a version that is not monospaced, which may be desirable for graphic design and general text rendering.

Becase the height of the characters is `5` pixels, PixelForge recommends the following settings for best results:
```
Recommended size: 5pt at 96 DPI

Best results at integer multiples:
   5pt
   10pt
   15pt
   20pt
   ...
```
