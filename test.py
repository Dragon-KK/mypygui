from src import mypygui

browser_window = mypygui.BrowserWindow()

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