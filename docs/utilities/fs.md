# fs

## URI

<div class="location">mypygui.core.fs.uri.URI</div>

### URI.Schema

<div class="property">
    <div class="property-name">URI.<span class="last_word">Schema</span><div class="property-type">Enum (static)</div></div>
    <div class="property-description">
    Currently recognized Schemas are
    <ul>
        <li>file
        <li>http
        <li>https
    </ul>
    </div>
</div>

### URI.schema

<div class="property">
    <div class="property-name">URI.<span class="last_word">schema</span><div class="property-type"><a href="#urischema">URI.Schema</div></div>
    <div class="property-description">The schema of the uri</div>
</div>

### URI.host

<div class="property">
    <div class="property-name">URI.<span class="last_word">host</span><div class="property-type">str</div></div>
    <div class="property-description">The host of the uri</div>
</div>

### URI.path

<div class="property">
    <div class="property-name">URI.<span class="last_word">path</span><div class="property-type">pathlib.Path</div></div>
    <div class="property-description">The path pertaining to the uri</div>
</div>

### URI.queries

<div class="property">
    <div class="property-name">URI.<span class="last_word">queries</span><div class="property-type">list[str]</div></div>
    <div class="property-description">Queries in the uri</div>
</div>

### URI.fragment

<div class="property">
    <div class="property-name">URI.<span class="last_word">fragment</span><div class="property-type">str</div></div>
    <div class="property-description">Fragments of the uri</div>
</div>

### URI.parent

<div class="property">
    <div class="property-name">URI.<span class="last_word">parent</span><div class="property-type"><a href="#uri">URI</a></div></div>
    <div class="property-description">The parent of the uri</div>
</div>

### URI.make

<div class="property">
    <div class="property-name">URI.<span class="last_word">make</span><div class="property-type">( ) -> <a href="#uri">URI</a></div></div>
    <div class="property-description">
        Creates a new uri relative to the current uri<br>
        NOTE: This function keeps in mind that http and file uris have to be handled differently<br>
        NOTE: This function is used by mypygui to handle urls present in the html<br>
        Parameters:
            <ul>
                <li> <code>uri_string : str</code> <br>
                The uri_string (or partial uri string in the case of local url)
            </ul>
        Returns:<br>
            The uri that was made (a uri relative to the current one)
    </div>
</div>

### URI.join

<div class="property">
    <div class="property-name">URI.<span class="last_word">join</span><div class="property-type">(*parts) → <a href="#uri">URI</a></div></div>
    <div class="property-description">
        Creates a new uri based on the parts given<br>
        Parameters:
            <ul>
                <li> <code>*parts : [...str]</code> <br>
            </ul>
        Returns:<br>
            The joined URI
    </div>
</div>

### URI.to_string

<div class="property">
    <div class="property-name">URI.<span class="last_word">to_string</span><div class="property-type">( ) → str</div></div>
    <div class="property-description">Converts the uri to a string</div>
</div>

### URI.from_uri_string

<div class="property">
    <div class="property-name">URI.<span class="last_word">from_uri_string</span><div class="property-type">classmethod (uri, _resolve_path?) → <a href="#uri">URI</a></div></div>
    <div class="property-description">
    Forms the uri using a string<br>
    Parameters:
        <ul>
            <li> <code>uri : str</code> <br>
            The string representation of the uri
            <li> <code>_resolve_path : bool</code> <br>
            Resolves the path of the given uri if set to true (False by default )
        </ul>
    Returns:<br>
        A uri from the string
    </div>
</div>

### URI.from_local_path_string

<div class="property">
    <div class="property-name">URI.<span class="last_word">from_local_path_string</span><div class="property-type">classmethod (path) → <a href="#uri">URI</a></div></div>
    <div class="property-description">
    Forms a uri using a path to the given local resource<br>
    NOTE: The paths must be absolute paths<br>
    Parameters:
        <ul>
            <li> <code>path : str</code> <br>
            The absolute path
        </ul>
    Returns:<br>
        A uri from the string
    </div>
</div>

<hr>

## Reading

<div class="location">mypygui.core.asynchronous.fs.reading</div>

### FileType

<div class="property">
    <div class="property-name last_word">FileType<div class="property-type">Enum</div></div>
    <div class="property-description">
    Currently recognized filetypes are
    <ul>
        <li>text
        <li>bytes
    </ul>
    </div>
</div>

### load

<div class="property">
    <div class="property-name"><span class="last_word">load</span><div class="property-type">(uri, file_type?) → any</div></div>
    <div class="property-description">
    Loads a file given a uri<br>
    NOTE: Will load files present both on the web or present locally
    NOTE: This process is synchronous<br>
    Parameters:
        <ul>
            <li> <code>uri : <a href="#uri">fs.URI</a></code> <br>
            URI of the resources that needs to be loaded
            <li> <code>file_type : <a href="#filetype">FileType</a></code> <br>
            The FileType of the resource (FileType.text as default)
        </ul>
    Returns:<br>
        The content
    </div>
</div>

### load_web

<div class="property">
    <div class="property-name"><span class="last_word">load_web</span><div class="property-type">(uri, file_type?) → any</div></div>
    <div class="property-description">
    Loads a given uri using <code>requests.get</code><br>
    NOTE: This process is synchronous<br>
    Parameters:
        <ul>
            <li> <code>uri : <a href="#uri">fs.URI</a></code> <br>
            URI of the resources that needs to be loaded
            <li> <code>file_type : <a href="#filetype">FileType</a></code> <br>
            The FileType of the resource (FileType.text as default)
        </ul>
    Returns:<br>
        The content
    </div>
</div>

### load_local

<div class="property">
    <div class="property-name"><span class="last_word">load_local</span><div class="property-type">(uri, file_type?) → any</div></div>
    <div class="property-description">
    Loads a file given a uri using <code>pathlib.Path.read_text</code> or <code>pathlib.Path.read_bytes</code> as needed<br>
    NOTE: This process is synchronous<br>
    Parameters:
        <ul>
            <li> <code>uri : <a href="#uri">fs.URI</a></code> <br>
            URI of the resources that needs to be loaded
            <li> <code>file_type : <a href="#filetype">FileType</a></code> <br>
            The FileType of the resource (FileType.text as default)
        </ul>
    Returns:<br>
        The content
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
