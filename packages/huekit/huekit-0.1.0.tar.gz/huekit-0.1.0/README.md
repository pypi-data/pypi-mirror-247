# HueKit

Huekit is a simple package which lets you style and color text. Unlike colorama and other python text color-izers, huekit also lets you style text, and has more color variety than colorama.

# How To Use

The following is a code block which will later be explained, showing how to use huekit:

```Python
from huekit imort huekit

print(huekit.color("red") + huekit.bgcolor("blue") + "This text is red (with a blue background)," + huekit.style("bold") + " And this text is bold!")
```

```from huekit import huekit```: import the library.

```huekit.color("red")"```: this is huekit's color function. For a full list of the avaliable colors, please run ```huekit.colors()```.

```huekit.bgcolor("blue")```: this is huekit's background color function. For a full list of the avaliable background colors, please run ```huekit.bgcolors()```.

```huekit.style("bold")```: this is huekit's style function. For a full list of the avaliable styles, please run ```huekit.styles()```.

# Notes

* ```huekit.color("white")``` resets all effects, doesn't just change the color to white.
* You can concatenate styles, background colors and colors together.