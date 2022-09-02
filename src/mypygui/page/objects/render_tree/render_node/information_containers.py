from .....util import Object, Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .....core.services.rendering.context import Context

class LayoutInformationContainer(Object):
    def __init__(self):
        self.reset()

    def reset(self):
        # the size of the content box
        self.content_height = 0
        self.content_width  = 0



        # This is the actual size of the content
        self.content_size_height = 0
        self.content_size_width = 0

        # the margins
        self.margin_top    = 0
        self.margin_right  = 0
        self.margin_bottom = 0
        self.margin_left   = 0

        # the paddings
        self.padding_top    = 0
        self.padding_right  = 0
        self.padding_bottom = 0
        self.padding_left   = 0

        # the border
        self.border_width = 0

        # the desired size of the element
        self.height = 0
        self.width  = 0
        #NOTE: THe height and width given will be transformed into border box model even if originally it was based on the content box

        # max size
        self.max_height = None
        self.max_width  = None

        # min size
        self.min_height = None
        self.min_width  = None 

        # the relative position of the element wrt to its master (the topleft)
        self.x = 0
        self.y = 0

        # The offset on the element
        self.offset_x = 0
        self.offset_y = 0



class RenderObjectType(Enum):
    text = Enum.auto(first=True)
    img  = Enum.auto()
    box  = Enum.auto()

class RenderInformationContainer(Object):
    def __init__(self, object_type : RenderObjectType = RenderObjectType.box):
        self.object_type = object_type
        '''The type of node the render node is'''
        self.context : Context = None
        '''Context is set on the paint call'''
        self.reset()

    def reset(self):
        self.foreground_color = ''
        self.font = ''

        self.x = 0
        '''the absolute x (compared to the nearest composite)'''
        self.y = 0
        '''the absolute y (compared to the nearest composite)'''

        self.offset_x = 0
        self.offset_y = 0

        self.width  = 0 
        '''The width of the padding box'''
        self.height = 0
        '''The height of the padding box'''

        self.border_bottom_left_radius  = 0
        '''The bottom_left border radius'''
        self.border_bottom_right_radius = 0
        '''The bottom_right border radius'''
        self.border_top_left_radius     = 0
        '''The top_left border radius'''
        self.border_top_right_radius    = 0
        '''The top_right border radius'''
        
        self.background_color = ''
        '''The color of the padding box'''

        self.border_stroke = 0
        '''The width of the border'''
        self.border_color = ''
        '''The color of the border'''      

LayoutInformationContainer.__register_serializer__()
LayoutInformationContainer.__register_deserializer__()
RenderInformationContainer.__register_serializer__()
RenderInformationContainer.__register_deserializer__()

