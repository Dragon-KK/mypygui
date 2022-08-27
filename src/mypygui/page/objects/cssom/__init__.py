from __future__ import annotations
from .style_sheet import StyleSheet
from ....util import Object

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...css.types import Rules
    from ..dom import DOMNode

# def _update_deeper_dict(updatee_dictionary : dict, updater_dictionary, needed_keys):
#     for key in (key for key in updater_dictionary if key in needed_keys):
#         if updatee_dictionary.get(key):
#             updatee_dictionary[key].update(updater_dictionary[key])
#         else:
#             updatee_dictionary[key] = updater_dictionary[key]
def _update_deeper_dict(updatee_dictionary : dict, updater_dictionary, needed_keys):
    for key in (key for key in updater_dictionary if key in needed_keys):
        updatee_dictionary.update(updater_dictionary[key])

class CSSOM(Object):
    def __init__(self, style_sheet : StyleSheet = None):
        self.stylesheet = StyleSheet() if style_sheet is None else style_sheet
        from .default_styles import selectors
        self.add_sheet(StyleSheet(selectors=selectors))

    #PERFORMANCE: Figure out a better way to do this in the future
    def get_styles(self, element : DOMNode) -> dict[str, Rules]:
        '''NOTE: tags < class < id | in terms of priority'''
        styles = {}
        '''dict<state : str, rules:Rules>'''
        # check for star match
        if self.stylesheet.selectors.get('*'):
            _update_deeper_dict(styles, self.stylesheet.selectors['*'], element.state)

        # check for tag match
        if self.stylesheet.selectors.get(element.tag):
            _update_deeper_dict(styles, self.stylesheet.selectors[element.tag], element.state)

        # check for class match
        for class_name in element.class_list:
            if self.stylesheet.selectors.get('.' + class_name):
                _update_deeper_dict(styles, self.stylesheet.selectors['.' + class_name], element.state)
        # check for id
        if element.id is not None:
            if self.stylesheet.selectors.get('#' + element.id):
                _update_deeper_dict(styles, self.stylesheet.selectors['#' + element.id], element.state)
        return styles
        
    def add_sheet(self, sheet : StyleSheet):
        '''Adds a sheet to the cssom'''
        for selector_name in sheet.selectors:
            for selector_state in sheet.selectors[selector_name]:
                self.stylesheet.add_ruleset(([(selector_name, selector_state)], sheet.selectors[selector_name][selector_state]))

    def clear(self):
        '''Resets the cssom'''
        self.stylesheet.clear()

CSSOM.__register_serializer__()
CSSOM.__register_deserializer__()