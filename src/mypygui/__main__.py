from . import *
import os
browser_window = BrowserWindow()

root = fs.URI.from_local_path_string(os.getcwd())

from .tools.dev_console import run_dev_console
run_dev_console(browser_window, root)

browser_window.on_close.await_result()