# This file is placed in the Public Domain.
#
#


import inspect
import time
import _thread


from ..command import Commands
from ..errors  import Errors
from ..event   import Event
from ..object  import Object
from ..storage import Storage
from ..thread  import Thread
from ..utility import name, spl


from .parse import parse


def __dir__():
    return (
        'command',
        'debug',
        'forever',
        'scan'
    )


def command(txt):
    evn = Event()
    evn.txt = txt
    parse(evn)
    Commands.handle(evn)
    evn.wait()
    return evn


def debug(txt):
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
           _thread.interrupt_main()


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def scan(pkg, modstr, initer=False) -> []:
    mods = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
        mods.append(module)
    return mods
