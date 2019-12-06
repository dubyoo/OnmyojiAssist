from MyHelper import *
from enum import Enum, unique
import logging


@unique
class Role(Enum):
    Unknown = 0
    Single = 1
    Driver = 2
    Passenger = 3


class Onmyoji:
    def __init__(self, onmyoji_assist, ts_plugin):
        self.onmyoji_assist = onmyoji_assist
        self.ts = ts_plugin
        self.role = Role.Unknown
        self._running = False
        self.count = 0

    def set_counts(self, count):
        self.count = count

    def terminate(self):
        self._running = False

    def run(self):
        self._running = True
        self.role_judgement()
        self.main_loop()

    def is_running(self):
        return self._running

    def thread_sleep(self, sleep_time, variable_time=0):
        if self._running:
            random_sleep(sleep_time, variable_time)
        if not self._running:
            logging.info("Onmyoji stopped")
            quit()

    def role_judgement(self):
        while self.role == Role.Unknown:
            self.role = Role.Single
            logging.info("Role judgement: %s" % self.role)
            # self.role = Role.Driver
            # self.role = Role.Passenger
            break

    def main_loop(self):
        # main loop of battle
        counter = 0
        while self._running:
            counter += 1
            logging.info('<------ Mission Start (%d)------>' % counter)
            # self.enter_battlefield()
            #
            # # detect if we are in the battle
            # while not self.is_in_the_battle():
            #     self.thread_sleep(500)
            # logging.debug('now we are in the battle')
            #
            # # detect if we finished
            # while self.is_in_the_battle():
            #     self.thread_sleep(500)
            # logging.debug('battle finished')
            # self.thread_sleep(2000)
            #
            # # bonus page
            # while not self.is_proxy_ready():
            #     logging.debug('bonus time ~~~')
            #     click_in_region(self.ts, *Region_Bonus)
            #     self.thread_sleep(500, 1000)
            # logging.debug('leave bonus page')
            logging.info('<------ Mission End (%d)------>' % counter)
            if self.count == counter:
                self.onmyoji_assist.ui.pushButton_stop.click()
                logging.info("Onmyoji mission task done")
                quit()
            self.thread_sleep(500)

    def enter_battlefield(self):
        pass

    def is_in_the_battle(self):
        # return self.ts.GetColor(*Coord_InTheBattle) == Color_InTheBattle
        pass
