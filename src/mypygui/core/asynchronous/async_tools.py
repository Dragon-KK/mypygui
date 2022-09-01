from __future__ import annotations
from abc import ABC
from .. import exceptions
from threading import Thread, Event
from ...logging import console

class Signal(Event):
    '''Basically just threading.Event'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Promise:
    ''':)'''

    #region constants
    ONGOING = 0
    '''The state of a promise which has not been resolved or cancelled'''
    SUCCESS = 1
    '''The state of a promise which has been resolved'''
    FAILURE = 2
    '''The state of a promise which has been cancelled'''
    #endregion

    def __init__(self):
        self.state = Promise.ONGOING
        '''The state of the promise'''

        self._success_handlers = set()
        '''Set of all functions subscribed to promise resolution'''

        self._error_handlers  = set()
        '''Set of all functions subscribed to promise cancellaion'''

        self.result = None
        '''The resolved value or the cancellation reason'''

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
        Subscribes to the resolution of the promise
        Parameters:
            callback : (result, purity?)
                NOTE: The purity is only given if `provide_purity` was set to True
            provide_purity : bool
                Set to True to know if the promise was resolved before the 'then' method was applied on it
        Returns:
            The same promise
        '''
        if self.state == Promise.ONGOING:
            self._success_handlers.add((callback, provide_purity))
            return self

        if self.state == Promise.SUCCESS:
            self._call_function((callback, provide_purity), False, self.result)

        return self

    def catch(self, callback : callable, provide_purity = False) -> Promise:
        '''
        Subscribes to the cancellation of the promise
        Parameters:
            callback : (reason, purity?)
                NOTE: The purity is only given if `provide_purity` was set to True
            provide_purity : bool
                Set to True to know if the promise was resolved before the 'catch' method was applied on it
        Returns:
            The same promise
        '''
        if self.state == Promise.ONGOING:
            self._error_handlers.add((callback, provide_purity))
            return self

        if self.state == Promise.FAILURE:
            self._call_function((callback, provide_purity), False, self.result)

        return self

    def await_result(self):
        '''Holds the thread till the promise has been cancelled or resolved'''
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