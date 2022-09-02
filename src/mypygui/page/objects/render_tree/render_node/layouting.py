from __future__ import annotations
from .....util import exceptions
from .... import css
from .....logging import console

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ... import RenderNode, DOMNode, RootRenderNode


INF = float('inf')

class layouter:

    @staticmethod
    def reflow_node(node : RenderNode, highest_reflowed_node : RenderNode = None):
        '''
        Recalculates the new layout according to the changes made to the current element
        It is suggested that a repaint be called on the element returned by reflow
        Recursively calls reflow on master till a master who hasnt been affected by the change has been attained
        NOTE: This function is only to be called by the render call handler
        '''
        if node.master is None: # The node is the root node
            return node.reflow(highest_reflowed_node)
            

        old_size = (node.layout_information.width,node.layout_information.height)
        old_margins = (node.layout_information.margin_left, node.layout_information.margin_top, node.layout_information.margin_right, node.layout_information.margin_bottom)  
        
        _1, size, _2, _3, _4 = layouter.layout_node(node, node.layout_information.y, node.layout_information.x, node.layout_information.margin_left, node.layout_information.margin_top, node.layout_information.y, node.layout_information.margin_top, node.master.layout_information.content_width)
                
        if old_size == size and old_margins == (node.layout_information.margin_left, node.layout_information.margin_top, node.layout_information.margin_right, node.layout_information.margin_bottom):
            return node.closest_relative
        else:
            return layouter.reflow_node(node.master_composite.composited_element, node)

    @staticmethod
    def set_render_info_size(node):
        node.render_information.height = node.layout_information.height
        node.render_information.width = node.layout_information.width

    @staticmethod
    def set_render_info_position(node):
        node.render_information.x = (node.master.render_information.x if not node.master.needs_composite else 0) + node.master.layout_information.border_width + (node.master.layout_information.padding_left if node.master.dom_node is node.dom_node.parent else 0) + node.layout_information.x
        node.render_information.y = (node.master.render_information.y if not node.master.needs_composite else 0) + node.master.layout_information.border_width + (node.master.layout_information.padding_top if node.master.dom_node is node.dom_node.parent else 0) + node.layout_information.y
        node.render_information.offset_x = node.layout_information.offset_x
        node.render_information.offset_x = node.layout_information.offset_x

    @staticmethod
    def layout_node(
        node : RenderNode,

        suggested_vertical_position : float, # The suggested line 
        suggested_horizontal_position : float, # The x position on the suggested line
        provided_margin_left : float, # The margin currently being provided on the left
        provided_margin_top : float, # The margin currently being provided on the top

        next_vertical_position : float, # The next line position
        next_line_provided_margin_top : float, # The margin currently provided on the next line
        
        line_end : float, # the content width (for inline elements where the width is set based on content size, the content width refers to the amount of space the inline element has on the line but note that this may not be the final content width)
        skip_node : RenderNode = None
    ) -> (
        (float, float), # Position
        (float, float), # Size
        (float, float), # Margin right and bottom
        bool, # Set to true if the element was positioned on a new line
        bool, # Set to true if the next element is to be positioned on a new line
    ):

        is_on_new_line = False
        next_on_new_line = False
        #region get sizes based on display
        if node is not skip_node:node.layout_information.reset()
    
        if node.dom_node.styles.display == css.Display.none: # If the element doesnt have to be displayed, just return since it doesnt have to be layouted
            node.dom_node._visible = False
            return (0, 0), (0, 0), (0, 0), False, False

        elif node.dom_node.styles.display == css.Display.block: # Block elements will go on a new line, force siblings to go on a new line and will implicitly fill as much width as possible
            
            if node is not skip_node:layouter.set_layout_information(node) # Set layotu information
            if node.layout_information.width is None: # If width was not explicitly set, it is implicitly set it
                node.layout_information.width = line_end - node.layout_information.margin_left - node.layout_information.margin_right
                node.layout_information.content_width  = node.layout_information.width - (2 * node.layout_information.border_width) - node.layout_information.padding_left - node.layout_information.padding_right if node.layout_information.width else 0        
                

            if node is not skip_node:layouter.validate_size(node) # Validate the size
            node.layout_information.x = node.layout_information.margin_left
            node.layout_information.y = next_vertical_position + max(node.layout_information.margin_top - next_line_provided_margin_top, 0)
            
            layouter.set_offset_1(node)
            layouter.set_render_info_position(node)
            content_size = layouter.layout_children(node, node.layout_information.content_width, skip_node=skip_node) if node is not skip_node else (node.layout_information.content_width, node.layout_information.content_height) # Layout the children
            if node.layout_information.height is None: # Implicitly set the height if needed
                node.layout_information.content_height = content_size[1]
                node.layout_information.height = node.layout_information.content_height + node.layout_information.padding_bottom + node.layout_information.padding_top + 2 * node.layout_information.border_width
                if node is not skip_node:layouter.validate_size(node) # Validate the size
                
            node.layout_information.content_size_width = content_size[0]
            node.layout_information.content_size_height = content_size[1]

            #region offset positions based on position
            layouter.set_offset_2(node)
            layouter.set_render_info_position(node)
            #endregion

            is_on_new_line = True
            next_on_new_line = True

        elif node.dom_node.styles.display == css.Display.inline: # Inline elements will implicitly set their max width to their master's max width and will finally set their width to their content size
            if node is not skip_node:layouter.set_layout_information(node)
            
            node.layout_information.x = suggested_horizontal_position + max(node.layout_information.margin_left - provided_margin_left, 0)
            node.layout_information.y = suggested_vertical_position + max(node.layout_information.margin_top - provided_margin_top, 0)
            layouter.set_render_info_position(node)
            if node is not skip_node:layouter.validate_size(node) # Validate any height or width set
            content_size = layouter.layout_children(node, node.layout_information.content_width if node.layout_information.content_width is not None else (line_end - node.layout_information.x), skip_node=skip_node) if node is not skip_node else (node.layout_information.content_width, node.layout_information.content_height)
            node.layout_information.content_height = content_size[1]
            node.layout_information.content_width = content_size[0]
            node.layout_information.width = node.layout_information.content_width + node.layout_information.padding_left + node.layout_information.padding_right + 2 * node.layout_information.border_width
            node.layout_information.height = node.layout_information.content_height + node.layout_information.padding_bottom + node.layout_information.padding_top + 2 * node.layout_information.border_width
            if node is not skip_node:layouter.validate_size(node) # Validate the size
            node.layout_information.content_size_height = content_size[1]
            node.layout_information.content_size_width = content_size[0]

            

        elif node.dom_node.styles.display == css.Display.inline_block: # Inline block elements are like inline elements but will implicitly fill as much width as possible and are allowed to have a say on their size
            if node is not skip_node:layouter.set_layout_information(node)
            
            node.layout_information.x = suggested_horizontal_position + max(node.layout_information.margin_left - provided_margin_left, 0)
            node.layout_information.y = suggested_vertical_position + max(node.layout_information.margin_top - provided_margin_top, 0)
            layouter.set_offset_1(node)
            layouter.set_render_info_position(node)
            if node.layout_information.width is None: # If width was not explicitly set, it is implicitly set it
                node.layout_information.width = line_end - node.layout_information.margin_left - node.layout_information.margin_right - suggested_horizontal_position if node.master.layout_information.content_width is not None and node.master.layout_information.content_width > 0 else 0
                node.layout_information.content_width  = node.layout_information.width - (2 * node.layout_information.border_width) - node.layout_information.padding_left - node.layout_information.padding_right if node.layout_information.width else 0        
            if node is not skip_node:layouter.validate_size(node) # Validate any height or width set
            content_size = layouter.layout_children(node, node.layout_information.content_width if node.layout_information.content_width is not None else (line_end - suggested_horizontal_position - node.layout_information.margin_left), skip_node=skip_node) if node is not skip_node else (node.layout_information.content_width, node.layout_information.content_height)
            
            if node.layout_information.height is None: # Implicitly set the height if needed
                node.layout_information.content_height = content_size[1]
                node.layout_information.height = node.layout_information.content_height + node.layout_information.padding_bottom + node.layout_information.padding_top + 2 * node.layout_information.border_width
                
            node.layout_information.content_size_height = content_size[1]
            node.layout_information.content_size_height = content_size[0]

            if node.layout_information.width is None: # Implicitly set the height if needed
                node.layout_information.content_width = content_size[0]
                node.layout_information.width = node.layout_information.content_width + node.layout_information.padding_left + node.layout_information.padding_right + 2 * node.layout_information.border_width
            if node is not skip_node:layouter.validate_size(node) # Validate the size
            #region offset positions based on position
            layouter.set_offset_2(node)
            layouter.set_render_info_position(node)
            #endregion
        
        elif node.dom_node.styles.display == css.Display.text:
            node.render_information.foreground_color = node.dom_node.styles.color
            node.render_information.font = (node.dom_node.styles.font_family, int(node.get_value(node.dom_node.styles.font_size, default=5)), node.dom_node.styles.font_weight)
            node.font.config(family=node.render_information.font[0], size=node.render_information.font[1], weight=node.render_information.font[2])
            
            content_width=0
            content_height=0
            node.layout_information.x = suggested_horizontal_position + max(node.layout_information.margin_left - provided_margin_left, 0)
            node.layout_information.y = suggested_vertical_position + max(node.layout_information.margin_top - provided_margin_top, 0)
            layouter.set_render_info_position(node)
            if node is not skip_node:
                layouter.set_layout_information(node)
                xs = node.dom_node.content.splitlines()
                if xs:
                    content_width = max(node.font.measure(i) for i in xs)
                    content_height = node.font.metrics('linespace') * (node.dom_node.content.count('\r') + 1)

            
            if node is not skip_node:layouter.validate_size(node) # Validate any height or width set
            content_size = (content_width, content_height) if node is not skip_node else (node.layout_information.content_width, node.layout_information.content_height)
            node.layout_information.content_height = content_size[1]
            node.layout_information.content_width = content_size[0]
            node.layout_information.width = node.layout_information.content_width + node.layout_information.padding_left + node.layout_information.padding_right + 2 * node.layout_information.border_width
            node.layout_information.height = node.layout_information.content_height + node.layout_information.padding_bottom + node.layout_information.padding_top + 2 * node.layout_information.border_width
            if node is not skip_node:layouter.validate_size(node) # Validate the size
            node.layout_information.content_size_height = content_size[1]
            node.layout_information.content_size_width = content_size[0]

        else:
            raise NotImplementedError('Unhandled display type', node.dom_node.styles.display)
        #endregion

        
        node.dom_node._visible = True
        layouter.set_render_info_size(node)
        node.after_layout()
        return (
            (node.layout_information.x, node.layout_information.y),
            (node.layout_information.width, node.layout_information.height),
            (node.layout_information.margin_right, node.layout_information.margin_bottom),
            is_on_new_line,
            next_on_new_line
        )

    @staticmethod
    def validate_size(node : RenderNode, validate_width = True, validate_height = True):
        '''Resets the height and width property taking into accound the min and max size'''
        if validate_width and node.layout_information.width is not None:
            if node.layout_information.width < node.layout_information.min_width:
                node.layout_information.width = node.layout_information.min_width
                node.layout_information.content_width  = node.layout_information.width - (2 * node.layout_information.border_width) - node.layout_information.padding_left - node.layout_information.padding_right if node.layout_information.width else 0
            elif node.layout_information.width > node.layout_information.max_width:
                node.layout_information.width = node.layout_information.max_width
                node.layout_information.content_width  = node.layout_information.width - (2 * node.layout_information.border_width) - node.layout_information.padding_left - node.layout_information.padding_right if node.layout_information.width else 0

        if validate_height and node.layout_information.height is not None:
            if node.layout_information.height < node.layout_information.min_height:
                node.layout_information.height = node.layout_information.min_height
                node.layout_information.content_height  = node.layout_information.height - (2 * node.layout_information.border_width) - node.layout_information.padding_top - node.layout_information.padding_bottom if node.layout_information.height else 0
            elif node.layout_information.height > node.layout_information.max_height:
                node.layout_information.height = node.layout_information.max_height
                node.layout_information.content_height  = node.layout_information.height - (2 * node.layout_information.border_width) - node.layout_information.padding_top - node.layout_information.padding_bottom if node.layout_information.height else 0

    @staticmethod
    def set_offset_1(node : RenderNode):
        '''Offsets the position of the element according to its left top right bottom values'''
        node.set_units()

        left = None
        right = 0
        top = None
        bottom = 0
        if node.dom_node.styles.position != css.Position.static: # Any non staticly positioned element is allowed to have a say in its position (by offsetting itself)
            left, right = node.get_value(node.dom_node.styles.left, None), node.get_value(node.dom_node.styles.right)
            top, bottom = node.get_value(node.dom_node.styles.top, None), node.get_value(node.dom_node.styles.bottom)
        node.layout_information.x += left if left is not None else -right
        node.layout_information.y += top if top is not None else -bottom
        
    @staticmethod
    def set_offset_2(node : RenderNode):
        node.layout_information.offset_x = node.get_value(node.dom_node.styles.transform_origin_x)
        node.layout_information.offset_y = node.get_value(node.dom_node.styles.transform_origin_y)


    @staticmethod
    def layout_children(
        node : RenderNode,
        line_end : float, # The content width of the parent
        skip_node : RenderNode = None
    ) -> (
        float, # The content width taken
        float, # The content height taken
    ):
        '''Layouts the children given some parameters'''
        child_current_line        = 0
        '''The y position of the current line'''
        child_current_position    = 0
        '''The x position on the current line'''
        child_current_margin_left = 0
        '''The margin currently accounted for on the left'''
        child_current_margin_top  = 0
        '''The margin currently accounted for on the top'''
        child_next_line           = 0
        '''The y position of the next line'''
        child_line_end            = line_end
        '''The end of the line'''
        child_next_line_margin_top = 0
        '''The margin accounted for the next line'''

        _curr_line_max_height = 0
        '''The maximum height without accounting for the margin top on the next line'''
        _curr_line_max_margined_height = 0
        '''The maximum height (while accounting the margin top on the next line)'''

        _curr_max_width = 0

        position, size, margin, on_new_line, forced_new_line = (0, 0), (0, 0), (0, 0), False, False

        # skip_node = None
        for child in node.dom_node.children:
            if child.render_node.master is not node:
                layouter.layout_node(child.render_node, 0, 0, 0, 0, 0, 0, child.render_node.master.layout_information.content_width, skip_node=skip_node)
                continue
            position, size, margin, on_new_line, force_new_line = layouter.layout_node(
                child.render_node, child_current_line, 
                child_current_position, 
                child_current_margin_left, 
                child_current_margin_top, 
                child_next_line, 
                child_next_line_margin_top, 
                line_end,
                skip_node=skip_node)

            if on_new_line: # If the element was placed on a new line
                _curr_max_width = max(_curr_max_width, position[0] + size[0] + margin[0])
                child_current_line = child_next_line # The current line is the next line
                child_current_position = 0 # The current position is updated a few lines later
                child_current_margin_top = child_next_line_margin_top # The margin currently provided on the top changes
                child_next_line = child_current_line # Update the next line
                child_next_line_margin_top = 0 # Update the next line margin top
                _curr_line_max_height = 0
                _curr_line_max_margined_height = 0


            height_taken = position[1] - child_current_line + size[1]
            _curr_line_max_height = max(_curr_line_max_height, height_taken)
            _curr_line_max_margined_height = max(_curr_line_max_margined_height, height_taken + margin[1])

            child_current_position = position[0] + size[0] + margin[0]
            child_current_margin_left = margin[0]
            child_next_line = child_current_line + _curr_line_max_margined_height
            child_next_line_margin_top = _curr_line_max_margined_height - _curr_line_max_height

            if force_new_line:
                _curr_line_max_height = 0
                _curr_line_max_margined_height = 0
                child_current_line        = child_next_line
                child_current_position    = 0
                child_current_margin_left = 0
                child_current_margin_top  = child_next_line_margin_top
        _curr_max_width = max(_curr_max_width, position[0] + size[0] + margin[0])
        return (_curr_max_width, child_next_line)

    @staticmethod
    def set_layout_information(node : RenderNode):
        '''Sets the layout information'''
        node.set_units()
        node.layout_information.is_set = True
        node.layout_information.padding_top = node.get_value(node.dom_node.styles.padding_top)
        node.layout_information.padding_right = node.get_value(node.dom_node.styles.padding_right)
        node.layout_information.padding_bottom = node.get_value(node.dom_node.styles.padding_bottom)
        node.layout_information.padding_left = node.get_value(node.dom_node.styles.padding_left)
        node.layout_information.margin_top = node.get_value(node.dom_node.styles.margin_top)
        node.layout_information.margin_right = node.get_value(node.dom_node.styles.margin_right)
        node.layout_information.margin_bottom = node.get_value(node.dom_node.styles.margin_bottom)
        node.layout_information.margin_left = node.get_value(node.dom_node.styles.margin_left)
        node.layout_information.border_width = node.get_value(node.dom_node.styles.border_width)
        if node.dom_node.styles.box_sizing == css.BoxSizing.border_box:
            node.layout_information.height = node.get_value(node.dom_node.styles.height, default=None)
            node.layout_information.width = node.get_value(node.dom_node.styles.width, default=None)

            node.layout_information.content_height = node.layout_information.height - (2 * node.layout_information.border_width) - node.layout_information.padding_bottom - node.layout_information.padding_top if node.layout_information.height is not None else None
            node.layout_information.content_width  = node.layout_information.width - (2 * node.layout_information.border_width) - node.layout_information.padding_left - node.layout_information.padding_right if node.layout_information.width is not None else None
            
            node.layout_information.max_height = node.get_value(node.dom_node.styles.max_height, default=None)
            node.layout_information.min_height = node.get_value(node.dom_node.styles.min_height, default=None)
            node.layout_information.max_height = node.layout_information.max_height if node.layout_information.max_height is not None else INF
            node.layout_information.min_height = node.layout_information.min_height if node.layout_information.min_height is not None else 0
            node.layout_information.max_width = node.get_value(node.dom_node.styles.max_width, default=None)
            node.layout_information.min_width = node.get_value(node.dom_node.styles.min_width, default=None)        
            node.layout_information.max_width = node.layout_information.max_width if node.layout_information.max_width is not None else INF
            node.layout_information.min_width = node.layout_information.min_width if node.layout_information.min_width is not None else 0 

        else:
            node.layout_information.content_height = node.get_value(node.dom_node.styles.height, default=None)
            node.layout_information.content_width  = node.get_value(node.dom_node.styles.width, default=None)

            node.layout_information.height = node.layout_information.content_height + (2 * node.layout_information.border_width) + node.layout_information.padding_bottom + node.layout_information.padding_top if node.layout_information.content_height is not None else None
            node.layout_information.width  = node.layout_information.content_width + (2 * node.layout_information.border_width) + node.layout_information.padding_left + node.layout_information.padding_right if node.layout_information.content_width is not None else None
            
            node.layout_information.max_height = node.get_value(node.dom_node.styles.max_height, default=None)
            node.layout_information.min_height = node.get_value(node.dom_node.styles.min_height, default=None)
            node.layout_information.max_height = node.layout_information.max_height + (2 * node.layout_information.border_width) + node.layout_information.padding_bottom + node.layout_information.padding_top if node.layout_information.max_height is not None else INF
            node.layout_information.min_height = node.layout_information.min_height + (2 * node.layout_information.border_width) + node.layout_information.padding_bottom + node.layout_information.padding_top if node.layout_information.min_height is not None else 0
            node.layout_information.max_width = node.get_value(node.dom_node.styles.max_width, default=None)
            node.layout_information.min_width = node.get_value(node.dom_node.styles.min_width, default=None)        
            node.layout_information.max_width = node.layout_information.max_width + (2 * node.layout_information.border_width) + node.layout_information.padding_left + node.layout_information.padding_right if node.layout_information.max_width is not None else INF
            node.layout_information.min_width = node.layout_information.min_width + (2 * node.layout_information.border_width) + node.layout_information.padding_left + node.layout_information.padding_right if node.layout_information.min_width is not None else 0
