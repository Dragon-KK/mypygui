# NOTE: Time timings have proven my Enums are the fastest
from ...util import Enum

class Position(Enum):
    '''How the element should be placed on the screen'''
    static   = Enum.auto(first=True) # Normal flow of the page
    relative = Enum.auto() # Get normal position but can move itself
    fixed    = Enum.auto() # Positioned wrt the body (cannot scroll)
    absolute = Enum.auto() # Position wrt the nearest relative parent
    #sticky   = Enum.auto() # Static until a point then fixed


class Display(Enum):
    '''How the element should be displayed'''
    none = Enum.auto(first=True)
    block = Enum.auto() # default width is to fill
    inline = Enum.auto() # width is the widht of content
    inline_block = Enum.auto() # best of both worlds
    text = Enum.auto()
    #flex = Enum.auto()
    #inlineFlex = Enum.auto()
    grid = Enum.auto() # not implemented
    #inlineGrid = Enum.auto()
    #flowRoot = Enum.auto()

class Overflow(Enum):
    hidden = Enum.auto(first=True)
    scroll = Enum.auto()

class Visibility(Enum):
    visible = Enum.auto(first=True)
    hidden  = Enum.auto()

class BoxSizing(Enum):
    content_box = Enum.auto(first=True)
    border_box  = Enum.auto()

class FontVariant(Enum):
    normal = Enum.auto(first=True)
    small_caps = Enum.auto()

class BorderWidth(Enum):
    medium = Enum.auto(first=True)
    thin = Enum.auto()
    thick = Enum.auto()

class BorderStyle(Enum):
    none = Enum.auto(first=True)
    dotted = Enum.auto()
    dashed = Enum.auto()
    solid = Enum.auto()
    double = Enum.auto()
    groove = Enum.auto()
    ridge = Enum.auto()
    inset = Enum.auto()
    outset = Enum.auto()
