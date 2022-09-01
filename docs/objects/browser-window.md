# BrowerWindow

<style>
    .property-name{
        background-color:cyan;
        color: black;
    }
</style>

```py
class BrowserWindow:...
```

Handles the loading and showing of pages

<div class="property-name">BrowserWindow.on_ready : <a href="../../utilities/asynchronous#Promise">Promise</a></div>
```py
BrowserWindow.on_ready : Promise
'''Resolved when the BrowserWindow has finished initializing'''
```

```py
BrowserWindow.on_close : Promise
'''Resolved when the BrowserWindow is going to close'''
```

```py
BrowserWindow.active_page : Page
'''Reference to the page that is being shown currently'''
```

```py
BrowserWindow.worker : Worker
'''A Service Provider that can be used by scripts'''
```

```py
BrowserWindow.resource_handler : ResourceHandler
'''Keeps track of all resources'''       
```

```py
BrowserWindow.layout_handler : LayoutHandler
'''The entity that deals with the rendering calls of the currently shown page'''      
```

```py
BrowserWindow.window_provider : WindowProvider
'''Entity that deals with context creation'''
```

```py
BrowserWindow.event_handler : EventHandler
'''Entity that deals with handling dom events'''
```

```py
BrowserWindow.tmp_store : Object
'''An object that persists between page loads'''
```

```py
def load_page(
        self,
        uri : fs.URI,
        persist = False
    ) -> Promise:
        '''Loads a page onto memory asynchrounoulsy given a uri'''
        

```

```py
def show_page(
        self,
        raw : str,
        uri : fs.URI
    ) -> Promise:
        '''
        Shows the page
        NOTE: Returns an always resolved promise
        '''
```

```py

    def end(self, reason = 'unknown'):
        '''
        Ends the application
        (by ending the window_provider)
        '''
```

```py
def execute_snippet(self, code_snippet,_locals, src = 'devtools'):
        '''Runs a code snippet on the active page'''
```
