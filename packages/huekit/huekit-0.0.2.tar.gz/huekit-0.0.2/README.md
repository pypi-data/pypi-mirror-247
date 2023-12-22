# HueKit

Huekit is a simple package which lets you style and color text. Unlike colorama and other python text color-izers, huekit also lets you style text, and has more color variety than colorama.

# How To Use

The following is a code block which will later be explained, showing how to use huekit:

```Python
import huekit

print(huekit.color("red") + "This text is red," + huekit.style("bold") + " And this text is bold!")
```

```import huekit```: import the library

```huekit.color("red") + "This text is red,"```: this is huekit's color function. you can concatenate any color to a string that you like, as long as it is in this list:

* black
* red
* green
* brown
* blue
* purple
* cyan
* light_gray
* dark_gray
* light_red
* light_green
* yellow
* light_blue
* light_purple
* light_cyan
* light_white

```huekit.style("bold") + " And this text is bold!"```: this is huekit's style function. you can concatenate any text style to a string that you like, as long as it is in this list:

* bold
* faint
* italic
* underline
* blink
* negative
* crossed
* end