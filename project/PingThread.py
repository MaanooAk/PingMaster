
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject

from threading import Thread
from time import sleep

from Pinger import OsPinger


class PingThread(Thread):

    def __init__(self, hostname, on_start, on_end, delay=0, pinger=None):
        Thread.__init__(self)
        self.hostname = hostname
        self.on_start = on_start
        self.on_end = on_end
        self.delay = delay
        self.pinger = pinger if pinger is not None else OsPinger()
        self.active = True

    def run(self):
        if self.delay > 0:
            sleep(self.delay)

        if not self.active:
            return

        # self.on_start(self.hostname)
        GObject.idle_add(self.on_start, self.hostname)

        result = self.pinger.ping(self.hostname)

        if not self.active:
            return

        # self.on_end(self.hostname, result)
        GObject.idle_add(self.on_end, self.hostname, result)


def ping_thread(hostname, on_start, on_end, delay=0) -> PingThread:

    t = PingThread(hostname, on_start, on_end, delay)
    t.start()

    return t
