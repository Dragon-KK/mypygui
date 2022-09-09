from __future__ import annotations
import gc
import traceback
from ..logging import console

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .objects import DOM, CSSOM, RenderTree
    from ..core.fs import URI
    from ..core.services.rendering import WindowProvider
    from ..core.services.resources import ResourceHandler
    from ..core.services.events import EventHandler
    from ..browser_window import BrowserWindow

from ..core.asynchronous import asyncify
from .clipboard import ClipBoard

class Page:
    def __init__(
        self,
        dom : DOM,
        cssom : CSSOM,
        render_tree : RenderTree,
        uri : URI,
        scripts : list,
        browser_window : BrowserWindow
    ):
        self.browser_window = browser_window
        '''Reference to the browser window'''
        self.dom = dom
        '''The dom'''
        self.cssom = cssom
        '''The cssom'''
        self.render_tree = render_tree
        '''The render tree'''
        self.uri = uri
        '''The uri'''
        self.scripts = scripts

        self.clipboard = ClipBoard(browser_window.window_provider.root)

        from .page_globals import get_globals
        self.script_globals = get_globals(self)

    def reload_page(self):
        '''
        Basically closes the page and shows it again (after reloading it)
        '''
        self.close()
        console.info('Reloading page')
        console.section()
        self.browser_window.load_page(self.uri).then(lambda resource:self.browser_window.show_page(*resource))
        

    def redirect(self, uri:fs.URI):
        '''
        _closes the page and then opens a new page
        '''
        self.close()
        console.info('Redirecting to', uri.to_string())
        console.section()
        self.browser_window.load_page(uri).then(lambda resource:self.browser_window.show_page(*resource))
        
    def close(self):
        '''
        Closes the page
        '''
        # PERFORMANCE: There seems to be a memory leak of approx 0.8 mb
        # https://stackoverflow.com/a/16423365
        # Perhaps its not a leak?
        self.script_globals['page_closed'].resolve(True)
        self.dom.root.remove(_remove_from_parent = False, _reflow=False)
        self.dom.root = None
        self.dom = None
        self.render_tree.root_render_node = None
        self.render_tree = None
        self.cssom.clear()
        self.cssom = None
        self.script_globals.clear()
        
        self.browser_window.resource_handler.reset()
        gc.collect()

        # new_snap = self.browser_window.tracemalloc.take_snapshot()
        # top_stats = new_snap.compare_to(self.browser_window.current_snapshot, 'lineno')

        # print("[ Top 10 differences ]")
        # for stat in top_stats[:15]:
        #     print(stat)

        # self.browser_window.current_snapshot = new_snap

    def end_application(self, reason = "Closed by script"):
        '''
        Closes the window
        '''
        self.browser_window.window_provider.end(reason)

    @lambda func:asyncify(func, name="Page.run_scripts")
    def run_scripts(self):
        for script in self.scripts:
            self.run_script(script)
    def run_script(self, script):
        try:
            exec(script[1], self.script_globals)
        except Exception as e:
            traceback.print_exc(file=console)
            console.debug('\n' + console.pop_written().strip().replace('<string>', script[0]))
            console.error(f'script `{script[0]}` execution failed')
    @classmethod
    def from_raw(cls, raw : str, uri : URI, browser_window : BrowserWindow):
        '''Loads a page given the raw html'''
        from .page_loader import create_from_raw
        return cls(
            *create_from_raw(raw, uri, browser_window),
        )