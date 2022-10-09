from .objects import DOM, CSSOM, RenderTree, RootRenderNode, RenderNode, DOMNode, TextRenderNode, ImageRenderNode, Image
from ..parsers import css_parser, html_parser, script_parser
from ..logging import console
from .objects.dom import Location
from ..util import functions
from ..core import fs
from .py_component import PyComponent
from ..core.services.events import Event
from .page_loader_helper import link_dom

def get_render_tree(dom) -> RenderTree:
    '''Creates the render tree'''
    render_tree = RenderTree(dom.root.render_node)
    dom.root.render_node.set_heirarchy()
    return render_tree

def create_from_raw(raw : str, uri : fs.URI, browser_window) -> tuple:
    '''Returns the arguments required for the creation of a page'''
    window_provider = browser_window.window_provider
    event_handler = browser_window.event_handler
    resource_handler = browser_window.resource_handler
    
    dom = DOM(html_parser.parse_dom_tree_from_raw(raw), Location(uri), Location(uri.parent))
    
    style_sheets = []
    anonymous_scripts_loaded = {'' : 0}
    scripts = []
    def handle_node(node, parent, args):
        try:
            node.event_emitter.event_handler = event_handler
            if node.tag == 'style':
                style_sheets.append(css_parser.parse_sheet_from_raw(node.content))
                return None
            elif node.tag == 'script':
                if node.attrs.src is not None:
                    scripts.append((dom.root_directory._uri.make(node.attrs.src).to_string(), script_parser.parse_script_from_raw(fs.load(dom.root_directory._uri.make(node.attrs.src), fs.FileType.text))))
                    return None
                scripts.append((f'anonymous {anonymous_scripts_loaded[""]}', script_parser.parse_script_from_raw(node.content.strip())))
                anonymous_scripts_loaded[''] += 1
                return None
            elif node.tag == 'component-definition':
                if node.attrs.src is None:
                    console.warn('Component definition does not link to any script')
                    return None
                g = {'PyComponent' : PyComponent}
                script = script_parser.parse_script_from_raw(fs.load(dom.root_directory._uri.make(node.attrs.src), fs.FileType.text))
                exec(script, g)
                if g.get('register_component') is None:
                    console.warn('Component definition does not define the required `register_component` function')
                    return None
                g['register_component'](window_provider.py_components)
                return None
            elif node.tag == 'link':
                if node.attrs.rel == 'stylesheet':
                    style_sheets.append(css_parser.parse_sheet_from_raw(fs.load(dom.root_directory._uri.make(node.attrs.href), fs.FileType.text)))
                return None
            elif node.tag == 'img':
                if node.attrs.src is not None:
                    node.image = resource_handler.request_resource(
                        uri = dom.root_directory._uri.make(node.attrs.src),
                        file_type = fs.FileType.bytes,
                        data_resolver = Image.handle_resource_request,
                        persist=True if node.attrs.persist is not None else False
                    )
                return None
            elif node.tag == 'title':
                dom.title = node.content
                return None
            else:
                return True
        except Exception as e:       
            import traceback
            traceback.print_exc()     
            console.error(f'Could not resolve resource `{node.tag}` | {e}')
    
    # Traverse tree over here get hold of css and scripts
    functions.traverse_tree(dom.root, handle_node)
    
    cssom = CSSOM()
    for style_sheet in style_sheets:
        cssom.add_sheet(style_sheet)
    link_dom(dom.root, cssom, window_provider = window_provider)
    render_tree = get_render_tree(dom)

    return (
        dom,
        cssom,
        render_tree,
        uri,
        scripts,
        browser_window
    )