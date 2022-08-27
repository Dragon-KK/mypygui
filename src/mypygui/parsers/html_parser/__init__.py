from ...page.objects.dom.dom_node import DOMNode, ClassList, StateContainer, RootDOMNode
from ...logging import console
from collections import deque
from ...util import Object
from ...core import fs
import unicodedata


from html.parser import HTMLParser as HTMLParserBase
class HTMLParser(HTMLParserBase):
    '''Parse the html'''
    tagInfo = {
        'meta' : (True,),
        'img' : (True,),
        'link' : (True,),
        'input' : (True,),
        0 : (False,)
    }
    '''
    Contains information on some elements which need special attention
    NOTE: tuple answers -> (isSelfClosing, )
    '''
    def __init__(self):
        super().__init__()
        self.stack : deque[DOMNode] = deque()
        self.stack.append(RootDOMNode(tag='html'))

    def parse(self, raw : str):
        '''Parses the html and returns the root element (the html element)'''
        self.feed(raw)
        self.close()
        return self.stack[0]

    def handle_starttag(self, tag, attrs):
        if HTMLParser.tagInfo.get(tag, HTMLParser.tagInfo[0])[0]: # If the element is self closing,
            return self.handle_startendtag(tag, attrs)
        if tag == 'html':return
        attrs = dict(attrs)
        elem = DOMNode(
            parent=self.stack[-1],
            tag=tag,
            attrs=Object(**attrs),
            id=attrs.get('id') if attrs.get('id') is not None else None,
            class_list=ClassList() if attrs.get('class') is None else ClassList(attrs['class'].split())
        )
        self.stack[-1].children.append(elem)
        self.stack.append(elem)

    def handle_endtag(self, tag):
        if tag == 'html':return
        if tag != self.stack[-1].tag:
            console.error(f"`{tag}` is trying to close `{self.stack[-1].tag}`")
            return
        self.stack.pop()        

    def handle_startendtag(self, tag, attrs):
        if tag == 'html':return
        attrs = dict(attrs)
        elem = DOMNode(
            parent=self.stack[-1],
            tag=tag,
            id=attrs.get('id') if attrs.get('id') is not None else None,
            attrs=Object(**dict((k,v if v is not None else True) for k,v in attrs.items())),
            class_list=ClassList() if attrs.get('class') is None else ClassList(attrs['class'].split())
        )
        self.stack[-1].children.append(elem)        

    def handle_data(self, data):
        xs = data.strip()
        if not xs:return
        self.stack[-1].content = xs

def parse_dom_tree_from_raw(raw : str) -> RootDOMNode:
    return HTMLParser().parse(raw)