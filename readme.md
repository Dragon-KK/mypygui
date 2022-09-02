# mypygui

github repo: <https://github.com/Dragon-KK/mypygui><br>
documentation: <https://dragon-kk.github.io/mypygui/>

## Dependencies

- python >= 3.10
- pillow >= 9.1.0
- tinycss2 >= 1.1.1
- webcolors >= 1.12
- colorama >= 0.4.4
- requests >= 2.28.1

## html

Any element that isn't supported will be treated like a div

Supported elements

- input
- img
- span

NOTE: Only text inside span elements are shown

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
<py-script src="./definitions.py"/>
<py-script src="./myscript.py"/>
```

eg: `myscript.py`

```py
document.get_element_by_id('my-elem')
```
