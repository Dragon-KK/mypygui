from typing import Any
from enum import IntEnum, auto
import colorama

class LEVEL(IntEnum):
    DEBUG   = auto()
    INFO    = auto()
    WARNING = auto()
    ERROR   = auto()

default_logger = {
    'section' : lambda count,char_type, kwargs: print(f"{colorama.Style.BRIGHT}{colorama.Fore.BLACK}{count * char_type}{colorama.Style.RESET_ALL}", **kwargs),
    'log' : lambda lvl,source,  msgs, kwargs : print(f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[LOG {colorama.Fore.BLACK}level:{lvl}{source}{colorama.Fore.WHITE}]{colorama.Style.RESET_ALL} {colorama.Fore.WHITE}{" ".join([str(i) for i in msgs])}{colorama.Style.RESET_ALL}', **kwargs),
    'debug' : lambda source, msgs, kwargs : print(f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[{colorama.Fore.GREEN}DEBUG{source}{colorama.Fore.WHITE}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTGREEN_EX}{" ".join([str(i) for i in msgs])}{colorama.Style.RESET_ALL}', **kwargs),
    'info' : lambda source, msgs, kwargs : print(f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[{colorama.Fore.BLUE}INFO{source}{colorama.Fore.WHITE}]{colorama.Style.RESET_ALL} {colorama.Fore.CYAN}{" ".join([str(i) for i in msgs])}{colorama.Style.RESET_ALL}', **kwargs),
    'warn' : lambda source, msgs, kwargs : print(f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[{colorama.Fore.LIGHTYELLOW_EX}WARNING{source}{colorama.Fore.WHITE}]{colorama.Style.RESET_ALL} {colorama.Fore.YELLOW}{" ".join([str(i) for i in msgs])}{colorama.Style.RESET_ALL}', **kwargs),
    'error' : lambda source, msgs, kwargs : print(f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}[{colorama.Fore.RED}ERROR{source}{colorama.Fore.WHITE}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTRED_EX}{" ".join([str(i) for i in msgs])}{colorama.Style.RESET_ALL}', **kwargs)
}

class Console:
    def __init__(self, source = ''):
        self.current_logging_level = 0
        self.logger = default_logger
        self._written = ''
        self.source = source

    def set_min_log_level(self, n : int):
        self.current_logging_level = n - 1

    def set_logger(self, new_logger):
        self.logger = new_logger

    def section(self, count = 10, char_type = '-', **kwargs):
        '''
        Sections the cmd line output
        '''
        self.logger['section'](count,char_type,kwargs)

    def log(self, *messages, level = 1, **kwargs):
        '''
        Logs messages at a given level, kwargs are given to the logger
        '''
        if self.current_logging_level < level:
            self.logger['log'](level, self.source, messages, kwargs)

    def debug(self, *messages, **kwargs): # lvl 1
        '''
        Logs messages at debug level, kwargs are given to the logger
        '''
        if self.current_logging_level < LEVEL.DEBUG:
            self.logger['debug'](self.source, messages, kwargs)

    def info(self, *messages, level = 1, **kwargs): # lvl 2
        '''
        Logs messages at info level, kwargs are given to the logger
        '''
        if self.current_logging_level < LEVEL.INFO:
            self.logger['info'](self.source, messages, kwargs)

    def warn(self, *messages, **kwargs): # lvl 3
        '''
        Logs messages at warning level, kwargs are given to the logger
        '''
        if self.current_logging_level < LEVEL.WARNING:
            self.logger['warn'](self.source, messages, kwargs)

    def error(self, *messages, **kwargs): # lvl 4
        '''
        Logs messages at error level, kwargs are given to the logger
        '''
        if self.current_logging_level < LEVEL.ERROR:
            self.logger['error'](self.source, messages, kwargs)

    def write(self, *args):
        '''Adds to whatever was written before the last pop_written'''
        for arg in args:
            self._written += arg

    def pop_written(self):
        xs = self._written
        self._written = ''
        return xs