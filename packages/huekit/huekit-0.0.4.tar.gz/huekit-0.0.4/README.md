# HueKit

Huekit is a simple package which lets you style and color text. Unlike colorama and other python text color-izers, huekit also lets you style text, and has more color variety than colorama.

# How To Use

The following is a code block which will later be explained, showing how to use huekit:

```Python
from huekit imort huekit

print(huekit.color("red") + "This text is red," + huekit.style("bold") + " And this text is bold!")
```

```from huekit import huekit```: import the library

```huekit.color("red") + "This text is red,"```: this is huekit's color function. For a full list of the avaliable colors, please run ```huekit.colors()```.

```huekit.style("bold") + " And this text is bold!"```: this is huekit's style function. For a full list of the avaliable styles, please run ```huekit.styles()```