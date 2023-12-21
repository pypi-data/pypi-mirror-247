## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install kolortext:

```bash
pip install kolortext
```

## How To Print Colored Text

We can print text with a colored foreground:

```python
from kolortext import fg

# Normal Colors
print(fg.red + "Red Text")
print(fg.green + "Green Text")
print(fg.blue + "Blue Text")

# Light Colors
print(fg.lightred + "Light Red Text")
print(fg.lightgreen + "Light Green Text")
print(fg.lightBlue + "Light Blue Text")
```

How it appears:

![Text with colored foreground](https://github.com/Samuel9360639/kolortext/assets/153092961/5a6a8095-690b-46a7-b44f-a525c3628199)

We can also print text with a colored background:

```python
from kolortext import bg

# Normal Colors
print(bg.red + "Red Background")
print(bg.green + "Green Background")
print(bg.blue + "Blue Background")

# Light Colors
print(bg.lightred + "Light Red Background")
print(bg.lightgreen + "Light Green Background")
print(bg.lightblue + "Light Blue Background")
```

How it appears:

![Text with colored background](https://github.com/Samuel9360639/kolortext/assets/153092961/a83d8644-3db8-47b8-a971-9c46db8339bf)

Available colors for fg and bg:

| Color                                                           | Name           |
|:---------------------------------------------------------------:|----------------|
| ![Black](https://placehold.co/15x15/000000/000000.png)          | black          |
| ![Red](https://placehold.co/15x15/800000/800000.png)            | red            |
| ![Green](https://placehold.co/15x15/008000/008000.png)          | green          |
| ![Yellow](https://placehold.co/15x15/808000/808000.png)         | yellow         |
| ![Blue](https://placehold.co/15x15/000080/000080.png)           | blue           |
| ![Magenta](https://placehold.co/15x15/800080/800080.png)        | magenta        |
| ![Cyan](https://placehold.co/15x15/008080/008080.png)           | cyan           |
| ![Grey](https://placehold.co/15x15/C0C0C0/C0C0C0.png)           | grey           |
| ![DarkGrey](https://placehold.co/15x15/808080/808080.png)       | darkgrey       |
| ![LightRed](https://placehold.co/15x15/FF0000/FF0000.png)       | lightred       |
| ![LightGreen](https://placehold.co/15x15/00FF00/00FF00.png)     | lightgreen     |
| ![LightYellow](https://placehold.co/15x15/FFFF00/FFFF00.png)    | lightyellow    |
| ![LightBlue](https://placehold.co/15x15/0000FF/0000FF.png)      | lightblue      |
| ![LightMagenta](https://placehold.co/15x15/FF00FF/FF00FF.png)   | lightmagenta   |
| ![LightCyan](https://placehold.co/15x15/00FFFF/00FFFF.png)      | lightcyan      |
| ![White](https://placehold.co/15x15/FFFFFF/FFFFFF.png)          | white          |

## How To Print Text Using Customized Colors

We can print using customized colors with Color Spaces RGB, HSL, HSV, Hex, CMYK:

```python
from kolortext import fg, bg, reset

# Foreground Colors
print(fg.rgb(255, 0, 0) + "Red Text")
print(fg.hsl(30, 100, 50) + "Orange Text")
print(fg.hsv(60, 100, 100) + "Yellow Text")
print(fg.hex('#00FF00') + "Green Text")
print(fg.cmyk(100, 0, 0, 0) + "Cyan Text" + reset.fg)

# Background Colors
print(bg.rgb(255, 0, 0) + "Red Background")
print(bg.hsl(30, 100, 50) + "Orange Background")
print(bg.hsl(60, 100, 100) + "Yellow Background")
print(bg.hex('#00FF00') + "Green Background")
print(bg.cmyk(100, 0, 0, 0) + "Cyan Background" + reset.bg)
```

How it appears:

![Text with customized Colors](https://github.com/Samuel9360639/kolortext/assets/153092961/dcb357cf-a177-4711-9d52-8665b4ca49f9)

## How To Print Stylized Text

We can also print Stylized Text:

```python
from kolortext import style

# Styles
print(style.bold + "Bold Text" + style.reset.bold)
print(style.underline + "Underlined Text" + style.reset.underline)
```

How it appears:

![Stylized text](https://github.com/Samuel9360639/kolortext/assets/153092961/6bf483ca-8317-40a3-8e46-7f10a9f049a2)

Available Styles:
    
    1. bold
    2. dim
    3. italic
    4. underline
    5. blink
    6. rapidblink
    7. reverse
    8. invisible
    9. strikethrough

Note: Some styles may not be supported in all terminals, and may have a different function.

## How To Use The Helper

### How To Check Color Model Values:

We can check whether HSL, HSV, Hex, CMYK and RGB Values are correct:

If the given color space values are correct, It will return True or else False.

```python
from kolortext.helper import check

# Valid Values
print(check.rgb(255,128,0))
print(check.hsl(30, 100, 50))
print(check.hsv(30, 100, 100))
print(check.hex('#FF8000'))
print(check.cmyk(0, 50, 100, 0))

# Invalid Values
print(check.rgb(300,128,0))
print(check.hsl(400, 100, 50))
print(check.hsv(400, 100, 100))
print(check.hex('#ZZ8000'))
print(check.cmyk(0, 50, 200, 0))
```

The first five lines will return True as the given values are correct but the next five will return False as the given values are incorrect.

### Valid Color Model Ranges:

    RGB = R - (0, 255), G - (0, 255), B - (0, 255)
    HSL = H - (0.0, 360.0), S - (0.0, 100.0), L - (0.0, 100.0)
    HSV = H - (0.0, 360.0), S - (0.0, 100.0), V - (0.0, 100.0)
    Hex = Numbers 0 to 9 and Letters A to F with Length of 6 Characters
    CMYK = C - (0, 100), M - (0, 100), Y - (0, 100), K - (0, 100) 

### How To Convert Values Between Color Models:

We can convert HSL, HSV, Hex, CMYK to RGB and back:

```python
from kolortext.helper import convert

# Color Models To RGB
print(convert.hsl_to_rgb(30, 100, 50))
print(convert.hsv_to_rgb(30, 100, 100))
print(convert.hex_to_rgb('#FF8000'))
print(convert.cmyk_to_rgb(0, 50, 100, 0))

# RGB To Color Models
print(convert.rgb_to_hsl(255, 0, 0))
print(convert.rgb_to_hsv(255, 128, 0))
print(convert.rgb_to_hex(255, 255, 0))
print(convert.rgb_to_cmyk(0, 255, 0))
```

Output:

![Convert color model values](https://github.com/Samuel9360639/kolortext/assets/153092961/16138648-f575-4cc5-a4f8-c4e04c1d0b89)

## Thanks!

### Contribute

If you have any suggestions, create a pull request [here](https://github.com/Samuel9360639/kolortext/pulls).

### Report Bugs 

If you find any bugs, please report them [here](https://github.com/Samuel9360639/kolortext/issues).