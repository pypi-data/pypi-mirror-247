# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1101,W0718,W0612,E0611


"output"


import queue
import textwrap
import threading


from .cache import Cache
from .wrap  import TextWrap


def __dir__():
    return (
            'Output',
           )


__all__  = __dir__()


wrapper = TextWrap()


class Output(Cache):

    def __init__(self):
        Cache.__init__(self)
        self.dostop = threading.Event()
        self.oqueue = queue.Queue()

    def gettxt(self, channel):
        txt = None
        try:
            che = self.cache.get(channel, None)
            if che:
                txt = che.pop(0)
        except (KeyError, IndexError):
            pass
        return txt

    def oput(self, channel, txt):
        if channel not in self.cache:
            self.cache[channel] = []
        self.oqueue.put_nowait((channel, txt))

    def out(self):
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                break
            if self.dostop.is_set():
                break
            txtlist = wrapper.wrap(txt)
            if len(txtlist) > 3:
                Output.extend(channel, txtlist)
                length = len(txtlist)
                self.say(
                         channel,
                         f"use !mre to show more (+{length})"
                        )
                continue
            _nr = -1
            for txt in txtlist:
                _nr += 1
                self.dosay(channel, txt)

    def dosay(self, channel, txt):
        raise NotImplementedError
