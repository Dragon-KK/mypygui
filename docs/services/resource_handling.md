# Resource Handling

## ResourceHandler([ServiceProvider](../service_provider))

<div class="location">mypygui.core.services.resource_handling.resource_handler.ResourceHandler</div>

### ResourceHandler.persisted_keys

<div class="property">
    <div class="property-name">ResourceHandler.<span class="last_word">persisted_keys</span><div class="property-type">set[str(<a href="../../utilities/fs#URI">fs.URI</a>)]</div></div>
    <div class="property-description">The set of all keys that were marked to persist between page loads</div>
</div>

### ResourceHandler.reset

<div class="property">
    <div class="property-name">ResourceHandler.<span class="last_word">reset</span><div class="property-type">( ) → None</div></div>
    <div class="property-description">
    Clears pending requests and resets any counters etc
    </div>
</div>

### ResourceHandler.release_all_resources

<div class="property">
    <div class="property-name">ResourceHandler.<span class="last_word">release_all_resources</span><div class="property-type">( ) → None</div></div>
    <div class="property-description">
        Releases all resources (including persisted resources)
    </div>
</div>

### ResourceHandler.release_resource

<div class="property">
    <div class="property-name">ResourceHandler.<span class="last_word">release_resource</span><div class="property-type">(request_key) → None</div></div>
    <div class="property-description">
        Releases a persisted resource given the resource key<br>
        NOTE: It is not recommended to use this<br>
        Parameters:
        <ul>
            <li> <code>resource_key</code> (use <code>ResourceHandler._get_request_key</code> to get this) <br>
        </ul>
    </div>
</div>

### ResourceHandler.request_resource

<div class="property">
    <div class="property-name">ResourceHandler.<span class="last_word">request_resource</span><div class="property-type">(uri?, file_type?, resource_key?, data_resolver?, persist?) → <a href="../../utilities/asynchronous#promise">Promise</a></div></div>
    <div class="property-description">
        Requests a resource<br>
        Parameters:
        <ul>
            <li> <code>uri : <a href="../../utilities/fs#URI">fs.URI</a></code><br>
                The uri that needs to be loaded
            <li> <code>file_type : <a href="../../utilities/fs#filetype">fs.FileType</a></code><br>
                The file type of the resource
            <li> <code>resource_key</a></code><br>
                A backup resource_key just in case a resource key could not be made from the uri (will never happen)
            <li> <code>data_resolver : (data) → any</a></code><br>
                A function that will modify the data to a more usable form
            <li> <code>persist : bool</code><br>
                Set persist to true to allow a resource to persist between page loads
        </ul>
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
