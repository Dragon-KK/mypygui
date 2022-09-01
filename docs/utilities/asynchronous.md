# Asynchronous

## Promise

<div class="location">mypygui.core.asynchronous.async_tools.Promise</div>

### Promise.state

<div class="property">
    <div class="property-name">Promise.<span class="last_word">state</span><div class="property-type">int</div></div>
    <div class="property-description">The state of the promise</div>
</div>

### Promise.result

<div class="property">
    <div class="property-name">Promise.<span class="last_word">result</span><div class="property-type">any</div></div>
    <div class="property-description">The resolved value or the cancellation reason. It is None by default</div>
</div>

### Promise.then

<div class="property">
    <div class="property-name">Promise.<span class="last_word">then</span><div class="property-type">(fn, provide_purity?) → <a href="#promise">Promise</a></div></div>
    <div class="property-description">
        Subscribes to the resolution of the promise <br>
        Parameters:
        <ul>
            <li> <code>callback : (result, purity?)</code><br>
            NOTE: The purity is only given if `provide_purity` was set to True
            <li> <code>provide_purity : bool</code> <br>
            Set to True to know if the promise was resolved before the 'then' method was applied on it
        </ul>
        Returns:<br>
        The same promise
    </div>
</div>

### Promise.catch

<div class="property">
    <div class="property-name">Promise.<span class="last_word">catch</span><div class="property-type">(fn, provide_purity?) → <a href="#promise">Promise</a></div></div>
    <div class="property-description">
        Subscribes to the cancellation of the promise <br>
        Parameters:
        <ul>
            <li> <code>callback : (reason, purity?)</code> <br>
            NOTE: The purity is only given if `provide_purity` was set to True
            <li> <code>provide_purity : bool</code> <br>
            Set to True to know if the promise was resolved before the 'catch' method was applied on it
        </ul>
        Returns:<br>
        The same promise
    </div>
</div>

### Promise.await_result

<div class="property">
    <div class="property-name">Promise.<span class="last_word">await_result</span><div class="property-type">( ) → None</div></div>
    <div class="property-description">Holds the thread till the promise has been cancelled or resolved</div>
</div>

### Promise.resolve

<div class="property">
    <div class="property-name">Promise.<span class="last_word">resolve</span><div class="property-type">(result : any) → None</div></div>
    <div class="property-description">Resolves the promise</div>
</div>

### Promise.cancel

<div class="property">
    <div class="property-name">Promise.<span class="last_word">cancel</span><div class="property-type">(reason : any) → None</div></div>
    <div class="property-description">Cancels the promise</div>
</div>

### Promise.ONGOING

<div class="property">
    <div class="property-name">Promise.<span class="last_word">ONGOING</span><div class="property-type">int (static)</div></div>
    <div class="property-description">The state of a promise which has not been resolved or cancelled</div>
</div>

### Promise.SUCCESS

<div class="property">
    <div class="property-name">Promise.<span class="last_word">SUCCESS</span><div class="property-type">int (static)</div></div>
    <div class="property-description">The state of a promise which has been resolved</div>
</div>

### Promise.FAILURE

<div class="property">
    <div class="property-name">Promise.<span class="last_word">FAILURE</span><div class="property-type">int (static)</div></div>
    <div class="property-description">The state of a promise which has been cancelled</div>
</div>

<hr>

## Signal

<div class="location">mypygui.core.asynchronous.async_tools.Signal</div>
<div class="property-description" style="margin-top:1rem">
    Basically just threading.Event
</div>

<hr>

## Miscellaneous Functions

<div class="location">mypygui.core.asynchronous.async_tools</div>
<div class="property">
    <div class="property-name last_word">asynchronously_run<div class="property-type">(fn, args?, kwargs?, daemon?, name?) → None</div></div>
    <div class="property-description">
    Runs the provided function on a new thread<br>
    NOTE: Setting `daemon` to False will allow the thread to run even after the main thread has ended
    </div>
</div>

<hr>

## Decorators

### thenify

<div class="property">
    <div class="property-name"><span class="last_word">thenify</span><div class="property-type">(fn, name?) → fn</div></div>
    <div class="property-description">
        Runs the function on a new thread whenever it is called and returns a promise that will get resolved when function finishes execution <br>
        NOTE: Raise an exception to cancel the promise from within the function <br>
        NOTE: The promise will not be provided to the thenified function <br>
    </div>
</div>

### promisify

<div class="property">
    <div class="property-name"><span class="last_word">promisify</span><div class="property-type">(fn, name?) → fn</div></div>
    <div class="property-description">
        Runs the function on a new thread whenever it is called and returns a promise that will get resolved when function finishes execution
        NOTE: The function must take in a parameter called `_promise` which contains the promise that is given in place of the funciton
        NOTE: The function must resolve or cancel the promise on its own
    </div>
</div>

### asyncify

<div class="property">
    <div class="property-name"><span class="last_word">asyncify</span><div class="property-type">(fn, name?) → fn</div></div>
    <div class="property-description">
        Marks a function to be run asynchronously (does not create any promises)
    </div>
</div>

<hr>

<style>
    .last_word{
        color : orangered !important;
    }
    .property-description{
        font-size:1.2em;
    }
    h2{
        font-size: 2em;
        margin: 0 !important;
        color : white;
        background-color : #444;
        padding: 0.3em;
        margin-top: 1em;
        border-left: solid 10px grey;
    }
    h3{
        visibility:hidden;
        height:0;
        margin:0;
    }
    .location{
        color : white;
        background-color : #444;
        padding: 0.5em 2em;
        font-size: 1em;
        font-family: monospace;
        border-left: solid 10px grey;
    }
    .property-name{
        font-family: monospace !important;
        color: darkcyan;
        margin: 1em 0 0 0;
        font-weight : bold;
        font-size: 1.5em;
    }
    .property-type::before{
        content: ' : ';
    }
    .property-type{
        display: inline;
        font-size:0.75em;
        color:yellowgreen;
    }
    li{
        padding-left:1rem;
    }
    .property{
        margin-left:1em;
        padding-left:0.5em;
        border-left:10px solid black;
    }
</style>
