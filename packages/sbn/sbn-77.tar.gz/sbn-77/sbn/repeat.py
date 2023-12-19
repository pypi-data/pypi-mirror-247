# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"repeater"


from .thread import Thread
from .timer  import Timer


from .utils.run import launch


def __dir__():
    return (
        'Repeater',
    )


__all__ = __dir__()
    

class Repeater(Timer):

    def run(self) -> Thread:
        ""
        thr = launch(self.start)
        super().run()
        return thr
