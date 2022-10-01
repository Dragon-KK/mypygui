from src import mypygui

browser_window = mypygui.BrowserWindow()

# TODO:SVG Support
# How do I want to implement this?
# It is a very very specific problem that I'm facing
# Maybe allow for a lower level 'shape' object? and just create a script that will convert svg into shape maybe?


# TODO:Animation Support
# How do I want to implement this?
# We obviously need some sort of an animation controller
# So another service that keeps track of time and will wait till the next required animation and when it does reach that point it will complete the task
# We do not need to allow support for animations thru scripts

# Maybe allow some premade animations like 'particle', 'bubble' etc. ?

my_uri = mypygui.fs.URI.from_local_path_string(__file__).parent.join('examples/html', 'index.html')
browser_window.on_ready\
.then(
    lambda _: browser_window.load_page(
        my_uri,
        persist=True
    ).then(
        lambda xs: browser_window.show_page(
            *xs
        ).then(
            lambda _: mypygui.logging.console.log(":)")
        )
    ).catch(
        lambda r:mypygui.logging.console.error('Load page error', r)
    )
).catch(
    lambda r: mypygui.logging.console.error('On ready error', r)
)
# from mypygui.tools.dev_console import run_dev_console
# run_dev_console(browser_window, my_uri.parent)
mypygui.logging.console.info('Closed because of',browser_window.on_close.await_result())