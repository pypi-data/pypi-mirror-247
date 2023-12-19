# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702,W0718,E1102,W0613


"reactor"


import queue
import threading
import _thread


from .broker import Broker
from .errors import Errors
from .object import Object


from .utils.run import launch


def __dir__():
    return (
        'Reactor',
    )


__all__ = __dir__()


class Reactor(Object):

    def __init__(self):
        Object.__init__(self)
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = False
        Broker.add(self)

    def callback(self, evt) -> None:
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        if self.threaded:
            evt._thrs.append(launch(func, evt))
        else:
            try:
                func(evt)
            except Exception as ex:
                Errors.add(ex)

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                self.callback(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put_nowait(evt)

    def register(self, typ, cbs) -> None:
        setattr(self.cbs, typ, cbs)

    def start(self) -> None:
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()
