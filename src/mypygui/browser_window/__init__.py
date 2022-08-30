from ..core.services.resource_handling import ResourceHandler
from ..core.services.layout_managing import LayoutHandler
from ..core.services.rendering import WindowProvider
from ..core.services.events import EventHandler
from ..core.services.worker import Worker
from ..core.asynchronous import Promise
from ..logging import console
from ..page import Page
from ..core import fs
# import tracemalloc
# tracemalloc.start()
class BrowserWindow:
    def __init__(
            self
        ):
        # self.tracemalloc = tracemalloc
        # self.current_snapshot = tracemalloc.take_snapshot()
        #region Promises
        self.on_ready          = Promise()
        '''Resolved when the browserWindow has finished initializing'''
        self.on_close          = Promise()
        '''Resolved when the browserWindow is going to end its process'''
        #endregion

        # self.allow_scripts = allow_scripts
        # '''Set to true if scripts are to be allowed'''
        # self.allowed_sources = allowed_sources
        # '''A set of allowed sources'''

        self.active_page : Page = None
        '''Reference to the page that is being shown currently'''

        self.worker = Worker()
        '''It do the work :)'''
        
        self.resource_handler = ResourceHandler()
        '''Keeps track of all resources'''

        self.layout_handler = LayoutHandler()
        '''The entity that deals with the rendering calls of the currently shown page'''

        self.window_provider = WindowProvider(self.layout_handler)
        '''Entity that deals with context creation'''
        self.window_provider.ended.then(self._on_window_provider_end) # Once the window_provider ends the application also must end

        self.event_handler = EventHandler()
        '''Entity that deals with handling dom events'''

        try:
            self.window_provider.run() # Start the window provider
            self.worker.run() # Start the resource manager      
            self.resource_handler.run()     
            self.layout_handler.run() # Start the layout handler
            self.event_handler.run()
            # LIMIT maybe if the renderer tkes to long to setup, to ready call is made before, maybe keep some kind of flag to stop this?
            console.info('Initialized browser window')
            self.on_ready.resolve(True)
        except Exception as e:
            console.error('Could not initialize browser_window')
            self.window_provider.end(reason='could not start')
            # Quit
            self.on_ready.cancel(e)

    def load_page(
        self,
        uri : fs.URI,
        persist = False
    ) -> Promise:
        '''Loads a page onto memory asynchrounoulsy given a uri'''
        return self.resource_handler.request_resource(
            uri = uri,
            file_type = fs.FileType.text,
            data_resolver = lambda raw : (raw, uri),
            persist=persist
            # NOTE: Any references that need to be passed from the browser_window to the page must be done from here
        )

    def show_page(
        self,
        raw : str,
        uri : fs.URI
    ) -> Promise:
        '''
        Shows the page
        NOTE: Returns an always resolved promise
        '''
        self.active_page = None # Set the active page
        self.active_page = Page.from_raw(raw, uri, self)

        # Reset service providers
        self.event_handler.reset() # Reset the event handler
        self.layout_handler.reset() # Reset the render call handler
        self.window_provider.reset(self.active_page.render_tree.root_render_node) # Reset the window_provider
        
        self.window_provider.set_title(self.active_page.dom.title) # Set the title of the new page
        
        # Layout and paint
        self.active_page.render_tree.layout() # This is sync
        self.active_page.render_tree.paint() # This is sync
        
        console.info('Showed page `{0}`'.format(self.active_page.dom.title))
        
        # Run scripts
        self.active_page.run_scripts() # This is async
        
        promise = Promise()
        promise.resolve(True)
        return promise
        
    def _on_window_provider_end(self, reason = 'gui'):
        '''Called when the window provider has ended'''
        if self.active_page is not None and self.active_page.script_globals['page_closed'].state == Promise.ONGOING:self.active_page.close()
        if self.worker.ended.state == Promise.ONGOING:self.worker.end()
        if self.resource_handler.ended.state == Promise.ONGOING:self.resource_handler.end()
        if self.layout_handler.ended.state == Promise.ONGOING:self.layout_handler.end()
        if self.event_handler.ended.state == Promise.ONGOING:self.event_handler.end()
        self.on_close.resolve(reason)
        
    def end(self, reason = 'unknown'):
        '''
        Ends the application
        (by ending the window_provider)
        '''
        if self.window_provider.ended.state == Promise.ONGOING:
            self.window_provider.end(reason)
        else:
            console.error('Tried to end the application when the window provider has already ended')
            self._on_window_provider_end(reason)
