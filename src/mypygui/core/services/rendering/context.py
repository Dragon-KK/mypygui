from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .composite import Composite


class Context:
    def __init__(self, parent_composite : Composite = None):
        self.box_token : int = -1
        '''The id of the box drawn'''
        self.bnd_token : int = -1
        '''The id of the bounds'''
        self.img_token : int = -1
        '''The id of the image drawn'''
        self.txt_token : int = -1
        '''The id of the text drawn'''