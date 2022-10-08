from __future__ import annotations
from .....util import Object, functions
from .... import css

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ... import CSSOM, DOMNode

class StyleContainer(Object):
    '''Contains the styles related to an element'''

    def __init__(
        self,
        background_color           : css.ColorValue       = None,
        border_width               : css.literals.BorderWidth  = None,
        border_bottom_left_radius  : css.DimensionalValue = None,
        border_bottom_right_radius : css.DimensionalValue = None,
        border_top_left_radius     : css.DimensionalValue = None,
        border_top_right_radius    : css.DimensionalValue = None,
        border_style               : css.literals.BorderStyle = None,
        border_color               : css.ColorValue       = None,
        color                      : css.ColorValue       = None,
        # opacity                    : css.NumberValue      = None,
        display                    : css.literals.Display = None,
        position                   : css.literals.Position  = None,
        z_index                    : css.NumberValue      = None,
        visibility                 : css.literals.Visibility  = None,
        box_sizing                 : css.literals.BoxSizing  = None,
        top                        : css.DimensionalValue = None,
        right                      : css.DimensionalValue = None,
        bottom                     : css.DimensionalValue = None,
        left                       : css.DimensionalValue = None,
        aspect_ratio               : (css.NumberValue, css.NumberValue) = None,
        height                     : css.DimensionalValue = None,
        width                      : css.DimensionalValue = None,
        max_heigth                 : css.DimensionalValue = None,
        max_width                  : css.DimensionalValue = None,
        min_height                 : css.DimensionalValue = None,
        min_width                  : css.DimensionalValue = None,
        font_family                : list[css.CSSStringValue]   = None,
        font_size                  : css.DimensionalValue = None,
        font_weight                : css.Number  = None,
        font_variant               : css.literals.FontVariant  = None,
        margin_bottom              : css.DimensionalValue = None,
        margin_left                : css.DimensionalValue = None,
        margin_right               : css.DimensionalValue = None,
        margin_top                 : css.DimensionalValue = None,
        padding_bottom             : css.DimensionalValue = None,
        padding_left               : css.DimensionalValue = None,
        padding_right              : css.DimensionalValue = None,
        padding_top                : css.DimensionalValue = None,
        transform_origin_y         : css.DimensionalValue = None,
        transform_origin_x         : css.DimensionalValue = None,
        overflow_x                 : css.literals.Overflow  = None,
        overflow_y                 : css.literals.Overflow  = None,        
    ):
        if background_color is not None:self.background_color : css.ColorValue = background_color
        
        #---------
        
        if border_width is not None:self.border_width : css.literals.BorderWidth = border_width
        
        if border_bottom_left_radius is not None:self.border_bottom_left_radius  : css.DimensionalValue = border_bottom_left_radius
        if border_bottom_right_radius is not None:self.border_bottom_right_radius : css.DimensionalValue = border_bottom_right_radius
        if border_top_left_radius is not None:self.border_top_left_radius     : css.DimensionalValue = border_top_left_radius
        if border_top_right_radius is not None:self.border_top_right_radius    : css.DimensionalValue = border_top_right_radius
        
        if border_style is not None:self.border_style : css.literals.BorderStyle = border_style
        if border_color is not None:self.border_color : css.ColorValue = border_color

        #--------

        if color is not None:self.color : css.ColorValue = color
        # if opacity is not None:self.opacity : css.DimensionalValue = opacity
        if display is not None:self.display : css.literals.Display = display
        if position is not None:self.position : css.literals.Position = position
        if z_index is not None:self.z_index : css.DimensionalValue = z_index
        if visibility is not None:self.visibility : css.literals.Visibility = visibility
        if box_sizing is not None:self.box_sizing : css.literals.BoxSizing = box_sizing
        
        #--------

        if top is not None:self.top : css.DimensionalValue = top
        if right is not None:self.right : css.DimensionalValue = right
        if bottom is not None:self.bottom : css.DimensionalValue = bottom
        if left is not None:self.left : css.DimensionalValue = left
        
        if aspect_ratio is not None:self.aspect_ratio : (css.NumberValue, css.NumberValue) = aspect_ratio
        if height is not None:self.height : css.DimensionalValue = height
        if width is not None:self.width : css.DimensionalValue = width
        if max_heigth is not None:self.max_heigth : css.DimensionalValue = max_heigth
        if max_width is not None:self.max_width : css.DimensionalValue = max_width
        if min_height is not None:self.min_height : css.DimensionalValue = min_height
        if min_width is not None:self.min_width : css.DimensionalValue = min_width
        
        #-------

        #LIMIT: Font weight based on numbers are not accepted
        if font_family is not None:self.font_family : list[css.CSSStringValue] = font_family
        if font_size is not None:self.font_size : css.DimensionalValue = font_size
        if font_weight is not None:self.font_weight : css.NumberValue = font_weight
        if font_variant is not None:self.font_variant : css.literals.FontVariant = font_variant
        
        #---------

        if margin_bottom is not None:self.margin_bottom : css.DimensionalValue = margin_bottom
        if margin_left is not None:self.margin_left : css.DimensionalValue = margin_left
        if margin_right is not None:self.margin_right : css.DimensionalValue = margin_right
        if margin_top is not None:self.margin_top : css.DimensionalValue = margin_top
        
        #---------

        if padding_bottom is not None:self.padding_bottom : css.DimensionalValue = padding_bottom
        if padding_left is not None:self.padding_left : css.DimensionalValue = padding_left
        if padding_right is not None:self.padding_right : css.DimensionalValue = padding_right
        if padding_top is not None:self.padding_top : css.DimensionalValue = padding_top
        
        #----------

        if transform_origin_y is not None:self.transform_origin_y : css.DimensionalValue = transform_origin_y
        if transform_origin_x is not None:self.transform_origin_x : css.DimensionalValue = transform_origin_x
        
        #------------
        
        if overflow_x is not None:self.overflow_x : css.literals.Overflow = overflow_x
        if overflow_y is not None:self.overflow_y : css.literals.Overflow = overflow_y

    def _update(self, dictionary):
        '''Updates the styles with the styles in the dictionary'''
        #NOTE: This function is kinda unsafe ngl        
        self.__dict__.update(dictionary)

    def _get_dict(self):
        '''Returns all properties as a dict'''
        return {
            "background_color" : self.background_color,
            "border_width" : self.border_width,
            "border_bottom_left_radius" : self.border_bottom_left_radius,
            "border_bottom_right_radius" : self.border_bottom_right_radius,
            "border_top_left_radius" : self.border_top_left_radius,
            "border_top_right_radius" : self.border_top_right_radius,
            "border_color" : self.border_color,
            "color" : self.color,
            "opacity" : self.opacity,
            "display" : self.display,
            "position" : self.position,
            "z_index" : self.z_index,
            "visibility" : self.visibility,
            "box_sizing" : self.box_sizing,
            "top" : self.top,
            "right" : self.right,
            "bottom" : self.bottom,
            "left" : self.left,
            "aspect_ratio" : self.aspect_ratio,
            "height" : self.height,
            "width" : self.width,
            "max_heigth" : self.max_heigth,
            "max_width" : self.max_width,
            "min_height" : self.min_height,
            "min_width" : self.min_width,
            "font_family" : self.font_family,
            "font_size" : self.font_size,
            "font_weight" : self.font_weight,
            "font_variant" : self.font_variant,
            "margin_bottom" : self.margin_bottom,
            "margin_left" : self.margin_left,
            "margin_right" : self.margin_right,
            "margin_top" : self.margin_top,
            "padding_bottom" : self.padding_bottom,
            "padding_left" : self.padding_left,
            "padding_right" : self.padding_right,
            "padding_top" : self.padding_top,
            "transform_origin_y" : self.transform_origin_y,
            "transform_origin_x" : self.transform_origin_x,
            "overflow_x" : self.overflow_x,
            "overflow_y" : self.overflow_y,
        }

    def _clear(self):
        '''Resets back to the default state'''
        self.background_color           = None
        self.border_width               = None
        self.border_bottom_left_radius  = None
        self.border_bottom_right_radius = None
        self.border_top_left_radius     = None
        self.border_top_right_radius    = None
        self.border_color               = None
        self.color                      = None
        self.opacity                    = None
        self.display                    = None
        self.position                   = None
        self.z_index                    = None
        self.visibility                 = None
        self.box_sizing                 = None
        self.top                        = None
        self.right                      = None
        self.bottom                     = None
        self.left                       = None
        self.aspect_ratio               = None
        self.height                     = None
        self.width                      = None
        self.max_heigth                 = None
        self.max_width                  = None
        self.min_height                 = None
        self.min_width                  = None
        self.font_family                = None
        self.font_size                  = None
        self.font_weight                = None
        self.font_variant               = None
        self.margin_bottom              = None
        self.margin_left                = None
        self.margin_right               = None
        self.margin_top                 = None
        self.padding_bottom             = None
        self.padding_left               = None
        self.padding_right              = None
        self.padding_top                = None
        self.transform_origin_y         = None
        self.transform_origin_x         = None
        self.overflow_x                 = None
        self.overflow_y                 = None

class Styles(StyleContainer):
    '''
    Stores the current styles of the element
    NOTE: It is itself a styleContainer which stores the true style of the element
    NOTE: Styles set through code take precedence
    '''
    __ignore__ = {'_element', '_cssom'}
    def __init__(self):
        super().__init__()
        self._code_set_styles : dict[css.PropertyName, css.Value] = {}
        '''The styles set through code'''
        self._element : DOMNode = None
        '''Reference to the element'''
        self._cssom : CSSOM = None
        '''Reference to the cssom'''

    def _set_reference(self, element : DOMNode, cssom : CSSOM):
        '''Sets reference to the element and the cssom'''
        self._element = element
        self._cssom = cssom

    def compute_true_styles(self, notify_element = True):
        '''
        Computes the styles of the element (by combining all of the rules applied)
        NOTE: This is expected to be called whenever a change is made to the state (if explicitly stated in the dom), or the classList of the element
        NOTE: Returns true if the added or removed classes affected the styles
        '''
        old = self._get_dict() # Get the currently set true styles
        styles = self._cssom.get_styles(self._element)
        styles.update(self._code_set_styles) # Update the queried styles with styles set by code
        for style in old: # Check if there was actually any need to compute true styles
            if styles.get(style) != old[style]: # If any of the newly calculated styles are different from what was set, reset styles
                self._clear()
                self._set_styles(styles, notify_element=notify_element) # Set styles                
                return True
        return False # No changes have been made to the true styles so return False

    def _set_styles(self, dictionary, notify_element = False):
        '''Updates the true styles and notfies the element if needed'''
        self._update(dictionary) # Updates the inner style container
        if notify_element: # Notify the element if needed
            self._element._on_true_style_change()

    def set_styles(self, notify_element = True, **dictionary):
        '''NOTE: This is only to be used by the scripts'''
        self._code_set_styles.update(dictionary) # Sets styles through code
        self._set_styles(dictionary, notify_element=notify_element)
