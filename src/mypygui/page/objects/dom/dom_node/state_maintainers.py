from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..dom_node import DOMNode

class ClassList(set):
    '''
    Stores the classes attributed to an element
    NOTE: The classes are stored unordered
    '''
    def __init__(self,*args):
        super().__init__(*args)
        self.element :DOMNode= None

    def add(self, cls, update_styles = True):
        if cls in self:return
        super().add(cls)
        self.element._on_class_change(added = cls, update_styles = update_styles)

    def remove(self, cls, update_styles = True):
        if cls in self:
            super().remove(cls)
        self.element._on_class_change(removed = cls, update_styles = update_styles)

    def toggle(self, cls, update_styles = True):
        if cls in self:
            self.remove(cls, update_styles = update_styles)
        else:
            self.add(cls, update_styles = update_styles)

    def __add__(self, cls):
        self.add(cls)

    def __sub__(self, cls):
        self.remove(cls)

class StateContainer(set):
    '''
    Stores the current state of the element
    NOTE: Order isn't of importance
    '''
    def __init__(self, *args):
        super().__init__(*args)
        self.element :DOMNode= None

    def add(self, state, update_styles = True):
        if state in self:return
        super().add(state)
        self.element._on_state_change(added = state, update_styles = update_styles)

    def toggle(self, state, update_styles = True):
        if state in self:
            self.remove(state, update_styles = update_styles)
        else:
            self.add(state, update_styles = update_styles)

    def remove(self, state, update_styles = True):
        if state in self:
            super().remove(state)
        self.element._on_state_change(removed = state, update_styles = update_styles)

    def __add__(self, state):
        self.add(state)

    def __sub__(self, state):
        self.remove(state)