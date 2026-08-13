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
These calculations work for `microfont_1d.png` and are probably the simplest to do. The X coordinate is directly related to the full ASCII character code.

```
x = get_ascii_code(character) * 3
y = 0
```

### 2D Calculations
These calculations work for `microfont_2d.png`. While they are slightly more complex, they allow for the source image to be a more reasonable aspect ratio. The X coordinate is based on the low nibble of the character code and the Y coordinate is based on the high nibble.

```
x = (get_ascii_code(character) & 0b1111) * 3
y = (get_ascii_code(character) >> 4) * 5
```
