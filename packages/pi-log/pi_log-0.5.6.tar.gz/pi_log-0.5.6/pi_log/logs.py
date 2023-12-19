"""
Logging module
"""
import logging
import os
from logging import Logger

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

ROOT = logging.getLogger("root")


def get_module_name():
    """
    Get the name of the module that calls the logs.py get_module_name() function
    """
    import inspect

    # frames = inspect.stack()
    n = None
    for i in range(len(inspect.stack())):
        frame = inspect.stack()[i]
        module = inspect.getmodule(frame[0])
        if module is None:
            continue
        if module:
            module_path = os.path.abspath(module.__file__)
            n = os.path.basename(os.path.dirname(module_path))
            if module.__name__ is not None:
                break
    return n


APP_ROOT_NAME = get_module_name()


def set_app_level(level: int | str):
    """Set the application logger level
    Args:
        level (int | str): log level
    """
    level = val_to_level(level)
    getLogger(APP_ROOT_NAME, level=level)


def get_app_logger(level: int | str = None) -> Logger:
    """Get the application logger level"""
    return getLogger(APP_ROOT_NAME, level=level)


def set_app_root(name: str) -> Logger:
    """Set the root logger name.
    By default the root logger name is already set to the name of the
    module that imports the logs.py module
    Args:
        name (str): logger name
    Returns:
        Logger: app root logger
    """
    global APP_ROOT_NAME
    APP_ROOT_NAME = name
    return getLogger(name)


def val_to_level(val: str | int) -> int:
    """Convert a string or int to a logging level
    Args:
        val (str | int): log level
    Returns:
        int: log level
    """
    if isinstance(val, str):
        oval = val
        val = val.strip()
        val = logging.getLevelName(val.upper())
        if not val or isinstance(val, str) and val.startswith("Level "):
            raise ValueError(f"invalid log level: {oval}")
    return val


def set_log_level(level: int | str, name: str = None):
    """Set logging to the specified level

    Args:
        level (int | str): log level
        name (str): logger name
    """
    level = val_to_level(level)
    if name is None:
        name = APP_ROOT_NAME
    log = logging.getLogger(name)
    log.setLevel(level)
    log.log(level, f"logging set to {level}")


def getLogger(name: str = None, level: int | str = None) -> Logger:
    """Get a logger with the specified name. If level is specified,
        set the log level.
        Typical usage:
            import logs
            log = logs.getLogger(__name__)
            log.info("Hello log world!")
    Args:
        name (str): logger name
        level (int | str): log level
    Returns:
        Logger: logger with the specified name
    """
    log = logging.getLogger(name)
    if level is not None:
        set_log_level(level, name)
    return log
