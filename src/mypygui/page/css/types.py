# Defines what a selector is, what a rule is, what a dimension is etc.
from typing import Tuple, Union
import abc
from ...util import Enum

# TODO: The types are not even used they are just confusing go back to this and like make it readable bro


class Unit(Enum):
    '''Specifies all the known units'''
    px               = Enum.auto(first=True)
    em               = Enum.auto()
    rem              = Enum.auto()
    viewport_height  = Enum.auto()
    viewport_width   = Enum.auto()
    null             = Enum.auto()
    
    master_height    = Enum.auto()
    master_width     = Enum.auto()
    self_height      = Enum.auto()
    self_width       = Enum.auto()


#region Property
PropertyName = str
'''The name of the css property'''
class ValueType(Enum):
    color = Enum.auto(first = True)
    dimension = Enum.auto()
    number = Enum.auto()
    string = Enum.auto()
CSSStringValue = str
'''A string'''
ColorValue = str
'''# Only hex colors supported for now (for the renderer)'''
NumberValue = float
'''A numerical value'''
DimensionalValue = Tuple[float, Unit]
'''Tuple containing rhe numerical value and the unit'''
Value = Union[DimensionalValue, ColorValue, CSSStringValue]
'''Defines what a value is'''
ValueCollection = list[Tuple[ValueType, Value]]
'''A collection of DimensionalValue (eg : in margin and border shorthands)'''
PropertyValue = (int, ValueCollection)
'''Size of the value collection and the value collection'''

#endregion

Rules = dict[PropertyName, PropertyValue]
'''Basically what is contained in a block in css (a dict containing the property values mapped to their values)'''

Selector = Tuple[str, str]
'''
A tuple containing the entity and the state of the entity for which the ruleset is to be applied
NOTE: Default state is `''` (empty string)
'''

RuleSet = Tuple[list[Selector], Rules]
'''A tuple containing the selectors which and the Rules that are to be applied on them'''