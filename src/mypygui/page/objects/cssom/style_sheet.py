from ...css.types import RuleSet, PropertyName, PropertyValue
from ....util import Object
from collections import OrderedDict

def _update_double_dict(updatee_dictionary : dict, key1 : str, key2 : str, updater_dictionary : dict):
    if updatee_dictionary.get(key1) is None:
        updatee_dictionary[key1] = OrderedDict()
    if updatee_dictionary[key1].get(key2) is None:
        updatee_dictionary[key1][key2] = {}
    updatee_dictionary[key1][key2].update(updater_dictionary)


class StyleSheet(Object):
    # LIMIT: Priority maintainance is kinda janky 
    # LIMIT: Serializing an ordered dict loses all the things stored like in it. Also like tuples and shit are stored as lists
    # Right now we say ;if the root selector had a rule applied to it before it has lower importance'
    def __init__(self, selectors : OrderedDict() = None):
        self.selectors : dict[str, dict[str, dict[PropertyName, PropertyValue]]] = OrderedDict() if selectors is None else selectors
        '''
        dict<
            selector_base : str,
            dict<
                state : str, 
                styles : dict<property_name : str, property_value : Value>
            >        
        >
        '''
    
    def add_ruleset(self, ruleset : RuleSet):
        '''
        Adds a ruleset
        '''
        for selector in ruleset[0]:
            _update_double_dict(self.selectors, selector[0], selector[1], ruleset[1])

    def clear(self):
        '''Clears all the data stored'''
        self.selectors.clear()

StyleSheet.__register_serializer__()
StyleSheet.__register_deserializer__()
StyleSheet.__register_serializer__(custom=OrderedDict, serializer=lambda v:{'__objecttype__' : 'OrderedDict', 'OrderedDict' : v})
StyleSheet.__register_deserializer__(custom=OrderedDict, deserializer=lambda v:OrderedDict(v))