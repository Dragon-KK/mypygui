# from ...
from ...logging import console

import cssutils
import logging
cssutils.log.setLevel(logging.FATAL) # Set the logging level to only log fatal errors

#TODONOW HAAAAAAAAAAA
#TODO: Rewrite css parser
# https://tinycss.readthedocs.io/en/latest/css3.html

from ...util import functions
from .property_validator import validate

def _rgba_to_hex(*rgba):
    return '#{:02x}{:02x}{:02x}'.format(*rgba)


from ...util import functions
from ...page import css
from ...logging import console

def _get_four_dimensional_values(value : css.PropertyValue) -> (css.DimensionalValue, css.DimensionalValue, css.DimensionalValue, css.DimensionalValue):
    for val in value[1]:
        if val[0] != css.ValueType.dimension and val[0] != css.ValueType.number:
            return None 
    if value[0] == 1:
        return (value[1][0][1], value[1][0][1], value[1][0][1], value[1][0][1])
    elif value[0] == 2:
        return (value[1][0][1], value[1][1][1], value[1][0][1], value[1][1][1])
    elif value[0] == 3:
        return (value[1][0][1], value[1][1][1], value[1][2][1], value[1][1][1])
    elif value[0] == 4:
        return (value[1][0][1], value[1][1][1], value[1][2][1], value[1][3][1])
    else:
        return None

def _validate_singleton_value(value : css.PropertyValue, property_type : css.ValueType):
    return value[0] == 1 and value[1][0][0] == property_type

def _warn_unsupported_value(property_name : str, property_value):
    console.warn(f'Unsopported value for `{property_name}`: `{property_value}`')
    return {}

def background(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `background` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.color):
        return {
            'background_color' : value[1][0][1]
        }
    
    _warn_unsupported_value('background', value)
    return {}


def background_color(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `background_color` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.color):
        return {
            'background_color' : value[1][0][1]
        }
    
    _warn_unsupported_value('background', value)
    return {}


def border(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border` value into a dict containing the needed property'''
    res = {}
    dimensions = []
    for val in value[1]:
        if val[0] == css.ValueType.color:
            res['border_color'] = val[1]
        elif val[0] == css.ValueType.string and css.literals.BorderStyle.contains(functions.snake_case(val[1])):
            res['border_style'] = css.literals.BorderStyle.str_to_enum(functions.snake_case(val[1]))
        elif val[0] == css.ValueType.dimension:
            res['border_width'] = val[1]
        elif val[0] == css.ValueType.number:
            res['border_width'] = val[1]
        else:
            _warn_unsupported_value('border', value)
            return {}
    return res

def border_width(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_width` value into a dict containing the needed property'''
    # Check if the string value 
    if _validate_singleton_value(value, css.ValueType.string) and css.BorderWidth.contains(functions.snake_case(value[1][0][1])):
        return {
            'border_width' : css.BorderWidth.str_to_enum(functions.snake_case(value[1][0][1]))
        }    
    _warn_unsupported_value('border_width', value)
    return {}

def border_radius(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_radius` value into a dict containing the needed property'''
    val = _get_four_dimensional_values(value)
    if val is not None:
        return {
            'border_top_left_radius' : val[0],
            'border_top_right_radius' : val[1],
            'border_bottom_left_radius' : val[2],
            'border_bottom_right_radius' : val[3],
        }

    _warn_unsupported_value('border_radius', value)
    return {}

def border_bottom_left_radius(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_bottom_left_radius` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'border_bottom_left_radius' : value[1][0][1]
        }
    
    _warn_unsupported_value('border_bottom_left_radius', value)
    return {}


def border_bottom_right_radius(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_bottom_right_radius` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'border_bottom_right_radius' : value[1][0][1]
        }
    
    _warn_unsupported_value('border_bottom_right_radius', value)
    return {}


def border_top_left_radius(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_top_left_radius` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'border_top_left_radius' : value[1][0][1]
        }
    
    _warn_unsupported_value('border_top_left_radius', value)
    return {}


def border_top_right_radius(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_top_right_radius` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'border_top_right_radius' : value[1][0][1]
        }
    
    _warn_unsupported_value('border_top_right_radius', value)
    return {}

def border_style(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_color` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.literals.BorderStyle.contains(functions.snake_case(value[1][0][1])):
        return {
            'border_color' : css.literals.BorderStyle.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('border_color', value)
    return {}

def border_color(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `border_color` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.color):
        return {
            'border_color' : value[1][0][1]
        }
    
    _warn_unsupported_value('border_color', value)
    return {}


def color(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `color` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.color):
        return {
            'color' : value[1][0][1]
        }
    
    _warn_unsupported_value('color', value)
    return {}


# def opacity(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
#     '''Parse the `opacity` value into a dict containing the needed property'''
#     if _validate_singleton_value(value, css.ValueType.number):
#         return {
#             'opacity' : value[1][0][1]
#         }
    
#     _warn_unsupported_value('opacity', value)
#     return {}


def display(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `display` value into a dict containing the needed property'''
    _translator = {

    }
    if _validate_singleton_value(value, css.ValueType.string) and css.Display.contains(functions.snake_case(value[1][0][1])):
        return {
            'display' : css.Display.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('display', value)
    return {}


def position(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `position` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.Position.contains(functions.snake_case(value[1][0][1])):
        return {
            'position' : css.literals.Position.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('position', value)
    return {}


def z_index(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `z_index` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.number):
        return {
            'z_index' : value[1][0][1]
        }
    
    _warn_unsupported_value('z_index', value)
    return {}


def visibility(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `visibility` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'visibility' : value[1][0][1]
        }
    
    _warn_unsupported_value('visibility', value)
    return {}


def box_sizing(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `box_sizing` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.BoxSizing.contains(functions.snake_case(value[1][0][1])):
        return {
            'box_sizing' : css.literals.BoxSizing.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('box_sizing', value)
    return {}


def top(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `top` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'top' : value[1][0][1]
        }
    
    _warn_unsupported_value('top', value)
    return {}


def right(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `right` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'right' : value[1][0][1]
        }
    
    _warn_unsupported_value('right', value)
    return {}


def bottom(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `bottom` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'bottom' : value[1][0][1]
        }
    
    _warn_unsupported_value('bottom', value)
    return {}


def left(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `left` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'left' : value[1][0][1]
        }
    
    _warn_unsupported_value('left', value)
    return {}


def height(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `height` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'height' : value[1][0][1]
        }
    
    _warn_unsupported_value('height', value)
    return {}


def width(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `width` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'width' : value[1][0][1]
        }
    
    _warn_unsupported_value('width', value)
    return {}


def max_heigth(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `max_heigth` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'max_heigth' : value[1][0][1]
        }
    
    _warn_unsupported_value('max_heigth', value)
    return {}


def max_width(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `max_width` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'max_width' : value[1][0][1]
        }
    
    _warn_unsupported_value('max_width', value)
    return {}


def min_height(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `min_height` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'min_height' : value[1][0][1]
        }
    
    _warn_unsupported_value('min_height', value)
    return {}


def min_width(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `min_width` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'min_width' : value[1][0][1]
        }
    
    _warn_unsupported_value('min_width', value)
    return {}


def font(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `font` value into a dict containing the needed property'''
    console.warn('css font shorthand not implemented')
    return {}


def font_family(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `font_family` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string):
       return {
           'font_family' : value[1][0][1].split(',')
       }
    _warn_unsupported_value('font_size', value)
    return {}


def font_size(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `font_size` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'font_size' : value[1][0][1]
        }
    
    _warn_unsupported_value('font_size', value)
    return {}


def font_weight(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `font_weight` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.number):
        return {
            'font_weight' : value[1][0][1]
        }
    
    _warn_unsupported_value('font_weight', value)
    return {}


def font_variant(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `font_variant` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.FontVariant.contains(functions.snake_case(value[1][0][1])):
        return {
            'font_variant' : css.FontVariant.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('font_variant', value)
    return {}


def margin(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `margin` value into a dict containing the needed property'''
    val = _get_four_dimensional_values(value)
    if val is not None:
        return {
            'margin_top' : val[0],
            'margin_right' : val[1],
            'margin_bottom' : val[2],
            'margin_left' : val[3],
        }

    _warn_unsupported_value('margin', value)
    return {}


def margin_bottom(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `margin_bottom` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'margin_bottom' : value[1][0][1]
        }
    
    _warn_unsupported_value('margin_bottom', value)
    return {}


def margin_left(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `margin_left` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'margin_left' : value[1][0][1]
        }
    
    _warn_unsupported_value('margin_left', value)
    return {}


def margin_right(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `margin_right` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'margin_right' : value[1][0][1]
        }
    
    _warn_unsupported_value('margin_right', value)
    return {}


def margin_top(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `margin_top` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'margin_top' : value[1][0][1]
        }
    
    _warn_unsupported_value('margin_top', value)
    return {}


def padding(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `padding` value into a dict containing the needed property'''
    val = _get_four_dimensional_values(value)
    if val is not None:
        return {
            'padding_top' : val[0],
            'padding_right' : val[1],
            'padding_bottom' : val[2],
            'padding_left' : val[3],
        }
    _warn_unsupported_value('padding', value)
    return {}


def padding_bottom(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `padding_bottom` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'padding_bottom' : value[1][0][1]
        }
    
    _warn_unsupported_value('padding_bottom', value)
    return {}


def padding_left(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `padding_left` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'padding_left' : value[1][0][1]
        }
    
    _warn_unsupported_value('padding_left', value)
    return {}


def padding_right(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `padding_right` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'padding_right' : value[1][0][1]
        }
    
    _warn_unsupported_value('padding_right', value)
    return {}


def padding_top(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `padding_top` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'padding_top' : value[1][0][1]
        }
    
    _warn_unsupported_value('padding_top', value)
    return {}


def transform_origin(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `transform_origin` value into a dict containing the needed property'''
    val = _get_four_dimensional_values(value)
    if val is not None:
        return {
            'transform_x' : val[0],
            'transform_y' : val[1]
        }
    _warn_unsupported_value('padding', value)
    return {}


def transform_origin_y(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `transform_origin_y` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'transform_origin_y' : value[1][0][1]
        }
    
    _warn_unsupported_value('transform_origin_y', value)
    return {}


def transform_origin_x(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `transform_origin_x` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.dimension):
        return {
            'transform_origin_x' : value[1][0][1]
        }
    
    _warn_unsupported_value('transform_origin_x', value)
    return {}

def overflow(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `overflow` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.Overflow.contains(functions.snake_case(value[1][0][1])):
        return {
            'overflow_x' : css.Overflow.str_to_enum(functions.snake_case(value[1][0][1])),
            'overflow_y' : css.Overflow.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('overflow_x', value)
    return {}


def overflow_x(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `overflow_x` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.Overflow.contains(functions.snake_case(value[1][0][1])):
        return {
            'overflow_x' : css.Overflow.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('overflow_x', value)
    return {}


def overflow_y(value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    '''Parse the `overflow_y` value into a dict containing the needed property'''
    if _validate_singleton_value(value, css.ValueType.string) and css.Overflow.contains(functions.snake_case(value[1][0][1])):
        return {
            'overflow_y' : css.Overflow.str_to_enum(functions.snake_case(value[1][0][1]))
        }
    
    _warn_unsupported_value('overflow_y', value)
    return {}

def validate(rule_name : css.PropertyName, rule_value : css.PropertyValue) -> dict[css.PropertyName, css.Value]:
    if rule_name == 'background':return background(rule_value)
    elif rule_name == 'background_color':return background_color(rule_value)
    elif rule_name == 'border':return border(rule_value)
    elif rule_name == 'border_radius':return border_radius(rule_value)
    elif rule_name == 'border_width':return border_width(rule_value)
    elif rule_name == 'border_bottom_left_radius':return border_bottom_left_radius(rule_value)
    elif rule_name == 'border_bottom_right_radius':return border_bottom_right_radius(rule_value)
    elif rule_name == 'border_top_left_radius':return border_top_left_radius(rule_value)
    elif rule_name == 'border_top_right_radius':return border_top_right_radius(rule_value)
    elif rule_name == 'border_style':return border_style(rule_value)
    elif rule_name == 'border_color':return border_color(rule_value)
    elif rule_name == 'color':return color(rule_value)
    # elif rule_name == 'opacity':return opacity(rule_value)
    elif rule_name == 'display':return display(rule_value)
    elif rule_name == 'position':return position(rule_value)
    elif rule_name == 'z_index':return z_index(rule_value)
    elif rule_name == 'visibility':return visibility(rule_value)
    elif rule_name == 'box_sizing':return box_sizing(rule_value)
    elif rule_name == 'top':return top(rule_value)
    elif rule_name == 'right':return right(rule_value)
    elif rule_name == 'bottom':return bottom(rule_value)
    elif rule_name == 'left':return left(rule_value)
    elif rule_name == 'height':return height(rule_value)
    elif rule_name == 'width':return width(rule_value)
    elif rule_name == 'max_heigth':return max_heigth(rule_value)
    elif rule_name == 'max_width':return max_width(rule_value)
    elif rule_name == 'min_height':return min_height(rule_value)
    elif rule_name == 'min_width':return min_width(rule_value)
    elif rule_name == 'font':return font(rule_value)
    elif rule_name == 'font_family':return font_family(rule_value)
    elif rule_name == 'font_size':return font_size(rule_value)
    elif rule_name == 'font_weight':return font_weight(rule_value)
    elif rule_name == 'font_variant':return font_variant(rule_value)
    elif rule_name == 'margin':return margin(rule_value)
    elif rule_name == 'margin_bottom':return margin_bottom(rule_value)
    elif rule_name == 'margin_left':return margin_left(rule_value)
    elif rule_name == 'margin_right':return margin_right(rule_value)
    elif rule_name == 'margin_top':return margin_top(rule_value)
    elif rule_name == 'padding':return padding(rule_value)
    elif rule_name == 'padding_bottom':return padding_bottom(rule_value)
    elif rule_name == 'padding_left':return padding_left(rule_value)
    elif rule_name == 'padding_right':return padding_right(rule_value)
    elif rule_name == 'padding_top':return padding_top(rule_value)
    elif rule_name == 'transform_origin':return transform_origin(rule_value)
    elif rule_name == 'transform_origin_y':return transform_origin_y(rule_value)
    elif rule_name == 'transform_origin_x':return transform_origin_x(rule_value)
    elif rule_name == 'overflow':return overflow(rule_value)
    elif rule_name == 'overflow_x':return overflow_x(rule_value)
    elif rule_name == 'overflow_y':return overflow_y(rule_value)
    else:
        console.warn(f'Unsopperted css property {rule_name}')





# TODO: Parsing of border style

#TODO: Parsing of percentages
def _get_percentage_unit(rule_name : str):
    print('unhandled percentage :(', rule_name)
    return css.Unit.master_width

def _get_unit(dimension : str):
    '''Returns the corresponing css unit given the dimension'''
    if   dimension == 'px' :return css.Unit.px
    elif dimension == 'em' :return css.Unit.em
    elif dimension == 'rem':return css.Unit.rem
    elif dimension == 'vw' :return css.Unit.viewport_width
    elif dimension == 'vh' :return css.Unit.viewport_height
    else:
        console.warn(f"Unkown dimension {dimension}")
        return css.Unit.null
    

def _normalize_values(rule_name, *values) -> css.PropertyValue:
    def normalize_value(val) -> css.Value:
        if val.type == cssutils.css.Value.COLOR_VALUE:return css.ValueType.color,_rgba_to_hex(val.red, val.green, val.blue, val.alpha)
        elif val.type == cssutils.css.Value.DIMENSION:return css.ValueType.dimension,(val.value, _get_unit(val.dimension))
        elif val.type == cssutils.css.Value.IDENT:return css.ValueType.string,val.value
        elif val.type == cssutils.css.Value.NUMBER:return css.ValueType.number,(val.value, 0)
        elif val.type == cssutils.css.Value.PERCENTAGE:return css.ValueType.dimension,(val.value, _get_percentage_unit(rule_name))
        else:raise NotImplementedError(f'Unhandled value type {val.type}')
    return (len(values), tuple(normalize_value(value) for value in values))

def _normalize_selectors(*selectors):
    def normalize_selector(selector):
        return selector.selectorText.partition(':')[::2]
    return list(normalize_selector(selector) for selector in selectors)

def parse_sheet_from_raw(raw : str) -> StyleSheet:
    # LIMIT Right now we only consider simple selectors ([name]:[state?] {<rules>})
    # NOTE: Parsing of shorthands are done over here itself
    # NOTE: THe normalizing for the style values (for each property) is done here too

    stylesheet = StyleSheet()
    parsed_intermediate = cssutils.parse.CSSParser().parseString(raw)

    for selector in parsed_intermediate.cssRules:
        style_declaration = selector.style
        rules = {}
        for property in style_declaration.getProperties():
            if not property.valid and (
                property.name != 'display' and property.value != 'text'
            ):
                
                console.warn(f'cssutils faced invalid property: {property}')
                continue
            rule_name = functions.snake_case(property.name)
            rule_value = _normalize_values(rule_name, *property.propertyValue)
            rules.update(validate(rule_name, rule_value))
        stylesheet.add_ruleset((_normalize_selectors(*selector.selectorList), rules))
    return stylesheet