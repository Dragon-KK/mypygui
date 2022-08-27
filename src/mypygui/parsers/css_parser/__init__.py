from ...page.objects.cssom import StyleSheet, CSSOM
from ...page import css
from ...util import functions
from ...logging import console

import tinycss2 as tc

from .property_validator import validate


def _get_rules(tokens : list):
    rules = {}
    current_property_name = ''
    current_property_value = []
    for token in tokens:
        if isinstance(token, tc.tokenizer.LiteralToken):
            if token.value == ';':
                rules.update(validate(current_property_name, current_property_value))
                current_property_name = ''
                current_property_value.clear()
        elif isinstance(token, tc.tokenizer.IdentToken):
            if not current_property_name:
                current_property_name = functions.snake_case(token.value)
                continue
            current_property_value.append(token)
        elif isinstance(
                token, 
                (tc.tokenizer.DimensionToken, tc.tokenizer.StringToken, tc.tokenizer.HashToken, tc.tokenizer.NumberToken, tc.tokenizer.FunctionBlock, tc.tokenizer.PercentageToken)
            ):
            current_property_value.append(token)
        elif not isinstance(token, tc.tokenizer.WhitespaceToken):
            console.warn('Unkown token type', token)

    return rules

def _get_selectors(tokens : list):
    selectors = []
    current_selector_text = ''
    next_is_state = False
    for token in tokens:
        if isinstance(token, tc.tokenizer.IdentToken):
            if next_is_state:
                selectors.append((current_selector_text, token.value))
                next_is_state = False
                current_selector_text = ''
            else:
                current_selector_text += token.value
        elif isinstance(token, tc.tokenizer.LiteralToken):
            if token.value == ':':
                next_is_state = True
            elif token.value == ',':
                selectors.append((current_selector_text, ''))
                current_selector_text = ''
            elif token.value == '.':
                current_selector_text += '.'
            elif token.value == '*':
                current_selector_text += '*'
        elif isinstance(token, tc.tokenizer.HashToken):
            current_selector_text += '#' + token.value
    if current_selector_text:
        selectors.append((current_selector_text, ''))
    return selectors

def parse_sheet_from_raw(raw : str) -> StyleSheet:
    style_sheet = StyleSheet()
    for rule in tc.parse_stylesheet(raw, skip_comments=True, skip_whitespace=True):
        selectors = _get_selectors(rule.prelude)
        rules = _get_rules(rule.content)
        style_sheet.add_ruleset((selectors, rules))

    return style_sheet