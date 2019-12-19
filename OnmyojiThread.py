from MyHelper import *
from enum import Enum, unique
import logging
import threading


@unique
class Role(Enum):
    Unknown = 0
    Single = 1
    Driver = 2
    Passenger = 3


class OnmyojiThread(threading.Thread):
    def __init__(self, onmyoji_assist, ts_plugin):
        super(OnmyojiThread, self).__init__()
        self._stop_event = threading.Event()
        self._onmyoji_assist = onmyoji_assist
        self._ts = ts_plugin
        self._role = Role.Unknown
        self._count = 0

    def set_count(self, count):
        self._count = count

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.__role_judgement()
        if self._role == Role.Unknown:
            self.__main_loop()
        elif self._role == Role.Single:
            self.__single_loop()
        elif self._role == Role.Driver:
            self.__driver_loop()
        elif self._role == Role.Passenger:
            self.__passenger_loop()

    def __emit_stop_signal(self):
        self.stop()
        self._onmyoji_assist.stop_signal.emit(int(self.getName()))

    def __sleep_or_quit(self, sleep_time, variable_time=0):
        if not self.is_stopped():
            random_sleep(sleep_time, variable_time)
        if self.is_stopped():
            logging.info("OnmyojiThread(%s) stopped" % self.getName())
            quit()

    def __role_judgement(self):
        self._role = Role.Unknown

    def __main_loop(self):
        counter = 0
        while not self.is_stopped():
            counter += 1
            logging.debug("Thread(%s) count %d" % (self.getName(), counter))
            if self._count == counter:
                logging.info("OnmyojiThread(%s) task done" % self.getName())
                self.__emit_stop_signal()
            self.__sleep_or_quit(500, 1000)

    def __single_loop(self):
        pass

    def __driver_loop(self):
        pass

    def __passenger_loop(self):
        pass

    def __enter_battlefield(self):
        return True

    def __is_in_the_battle(self):
        # return self.ts.GetColor(*Coord_InTheBattle) == Color_InTheBattle
        return True

    def unbind_window(self):
        logging.info('thread(%s) unBindWindow return: %d' % (self.getName(), self._ts.UnBindWindow()))
