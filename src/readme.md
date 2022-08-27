# mypygui

## Dependencies

- python >= 3.8
- tinycss2
- webcolors
- pillow

## opengl installation on windows

<https://www.youtube.com/watch?v=a4NVQC_2S2U>

## html

Any element that isn't supported will be treated like a div

Supported elements

- input

## CSS

NOTE: currently some of the supported css properties may not work exactly according to the spec

A list of all supported css properties

- `background-color`
- `border-width`
- `border-bottom-left-radius`
- `border-bottom-right-radius`
- `border-top-left-radius`
- `border-top-right-radius`
- `border-style`
- `border-color`
- `color`
<!-- - `opacity` -->
- `display`
- `position`
- `z-index`
- `visibility`
- `box-sizing`
- `top`
- `right`
- `bottom`
- `left`
- `height`
- `width`
- `max-heigth`
- `max-width`
- `min-height`
- `min-width`
- `font-family`
- `font-size`
- `font-weight`
- `font-variant`
- `margin-bottom`
- `margin-left`
- `margin-right`
- `margin-top`
- `padding-bottom`
- `padding-left`
- `padding-right`
- `padding-top`
- `transform-origin-x`
- `transform-origin-y`
- `overflow-x`
- `overflow-y`

## Script

All scripts will be executed globally

Some dom apis will be given to the scripts

```html
<pyscript src="./definitions.py"/>
<pyscript src="./myscript.py"/>
```

eg: `myscript.py`

```py
#@py-ignore
# Anything between consecutive py-ignore will not be executed at runtime
# Use this space to import files for intellisense etc.
#@py-ignore
```
