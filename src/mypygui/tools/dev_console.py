from ..logging import console
from ..core.asynchronous import Promise

def run_dev_console(browser_window, cwd):
    from .. import core, fs, logging, page, parsers, tools, util
    console.debug("Starting dev console")
    _locals = {
        'browser_window':browser_window,
        'core' : core,
        'fs' : fs,
        'logging' : logging,
        'page' : page,
        'parsers' : parsers,
        'tools' : tools,
        'util' : util,
        'cwd' : cwd
    }
    browser_window.on_close.then(lambda r:console.debug("Enter anything to stop session"))
    while browser_window.on_close.state == Promise.ONGOING:
        command = input(">> ")
        browser_window.execute_snippet(command, _locals)
