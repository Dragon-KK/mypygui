from __future__ import annotations
from ....util import Enum, Object

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....page.objects import DOMNode

class Event:
    class Types(Enum):
        click       = Enum.auto(first=True) # 'Button' use the button event in a handler for binding the mouse wheels and buttons.
        mouse_up    = Enum.auto() # 'ButtonRelease' instead of clicking a button, you can also trigger an event by releasing the mouse buttons.
        enter       = Enum.auto() # it actually works like <return> event that can be used to get the focus on a widget with mouse pointer
        key_press   = Enum.auto() # start the process or call the handler by pressing the key.
        key_release = Enum.auto() # start the process or call an event by releasing a key.
        leave       = Enum.auto() # use this event to track the mouse pointer when user switches from one widget to another widget.
        mouse_over  = Enum.auto() # 'Motion' track the event whenever the mouse pointer moves entirely within the application. 
        resize      = Enum.auto() # Called when the window size changes (only allowed to be attached to root)
        hover_start = Enum.auto() # An event defined by ourselves
        hover_end   = Enum.auto() # An event defined by ourselves
        scroll      = Enum.auto() # NOTE: This will only be dispatched by composited elements

    def __init__(self, type : str, target : DOMNode, propogate : bool, opposite_direction=False, **info):
        self.type = type
        self.propogate = propogate
        self.opposite_direction = opposite_direction
        self.target = target
        self.info = Object(**info)
