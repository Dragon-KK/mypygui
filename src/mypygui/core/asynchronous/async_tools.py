from __future__ import annotations
from abc import ABC
from .. import exceptions
from threading import Thread, Event
from ...logging import console

class Signal(Event):
    '''A renaming of the threading.Event'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Promise:
    ''':)'''

    #region constants
    ONGOING = 0
    SUCCESS = 1
    FAILURE = 2
    #endregion

    def __init__(self):
        self.state = Promise.ONGOING
        '''The state of the promise'''

        self._success_handlers = set()
        self._error_handlers  = set()

        self.result = None
        '''The result of the promise'''

    def resolve(self, result : any):
        '''Resolves the promise'''
        if self.state != Promise.ONGOING:
            raise exceptions.UnexpectedPromiseResolutionException(self, 'fulfilled' if self.state == Promise.SUCCESS else 'cancelled', 'resolve')

        self.state = Promise.SUCCESS
        self.result = result
        
        for func in self._success_handlers:
            self._call_function(func, True, result)

        self._success_handlers.clear()
        self._error_handlers.clear()


    def cancel(self, reason : any):
        '''Cancels the promise'''
        if self.state != Promise.ONGOING:
            raise exceptions.UnexpectedPromiseResolutionException(self, 'fulfilled' if self.state == Promise.SUCCESS else 'cancelled', 'cancel')

        self.state = Promise.FAILURE
        self.result = reason
        
        for func in self._error_handlers:
            self._call_function(func, True, reason)

        
        self._success_handlers.clear()
        self._error_handlers.clear()

    def _call_function(self, func : tuple, purity : bool, *args):
        '''Calls the function and sends the purity signal if required'''
        try:
            if func[1]: # If the function requires the purity
                func[0](*args, purity = purity)
            else:
                func[0](*args)
        except Exception as e:
            import traceback
            traceback.print_exc()
            console.error('Promise callback failure', e)
        

    def then(self, callback : callable, provide_purity = False) -> Promise:
        '''
        Subscribes to the promise
        NOTE: The callback function must take in a single parameter which will contain the result of the promise
        NOTE: Set `provide_purity` to True to get an additional parameter called `purity` which is set to False if the Promise was resolved before being subscribed to
        '''
        if self.state == Promise.ONGOING:
            self._success_handlers.add((callback, provide_purity))
            return self

        if self.state == Promise.SUCCESS:
            self._call_function((callback, provide_purity), False, self.result)

        return self

    def catch(self, callback : callable, provide_purity = False) -> Promise:
        '''
        Catches any errors or cancellations that arise
        NOTE: The callback function must take in a single parameter which will contain the reason for the cancellation
        NOTE: Set `provide_purity` to True to get an additional parameter called `purity` which is set to False if the Promise was resolved before being subscribed to
        '''
        if self.state == Promise.ONGOING:
            self._error_handlers.add((callback, provide_purity))
            return self

        if self.state == Promise.FAILURE:
            self._call_function((callback, provide_purity), False, self.result)

        return self

    def await_result(self):
        '''Will hold the thread until the promise has been fulfilled or cancelled'''
        result = Signal()
        self.then(lambda r: result.set()).catch(lambda r: result.set())
        result.wait()
        return self.result

def asynchronously_run(func, args = (), kwargs = {}, daemon = True, name='async'):
    '''
    Runs the provided function on a new thread
    NOTE: Setting `daemon` to False will allow the thread to run even after the main thread has ended
    '''
    Thread(target=func,name=name, args=args, kwargs=kwargs, daemon=daemon).start()