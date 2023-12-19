# This file is placed in the Public Domain.
#
#


"timer"


import datetime
import time


from sbn import Broker, Default, Event, Timer, construct, update


from sbn.utils import NoDate, day, now, to_time, to_day, get_day, get_hour
from sbn.utils import find, laps, launch, sync


def init():
    for fnm, obj in find("timer"):
        if "time" not in obj:
            continue
        diff = float(obj.time) - time.time()
        if diff > 0:
            bot = Broker.first()
            tmr = Timer(diff, bot.announce, obj.rest)
            launch(tmr.start)


def tmr(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('timer'):
            if "time" not in obj:
                continue
            lap = float(obj.time) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {laps(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers")
        return
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
             try:
                 seconds = int(word[1:])
             except:
                 event.reply("%s is not an integer" % seconds)
                 return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(day())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    event.time = target
    diff = target - time.time()
    event.reply("ok " +  laps(diff))
    event.show()
    event.result = []
    event.result.append(event.rest)
    timer = Timer(diff, event.show)
    update(timer, event)
    sync(timer)
    launch(timer.start)
