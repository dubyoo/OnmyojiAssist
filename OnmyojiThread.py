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
        logging.debug("Running thread(%s)" % self.getName())
        self.__role_judgement()
        self.__main_loop()

    def __emit_stop_signal(self):
        self.stop()
        self._onmyoji_assist.stop_signal.emit(int(self.getName()))

    def __sleep_or_quit(self, sleep_time, variable_time=0):
        if not self.is_stopped():
            random_sleep(sleep_time, variable_time)
        if self.is_stopped():
            logging.info("Thread(%s) stopped" % self.getName())
            quit()

    def __role_judgement(self):
        self._role = Role.Unknown
        start_time = time.clock()
        while self._role == Role.Unknown:
            self.__sleep_or_quit(500)
            self.__reject_xuan_shang()
            color_single = self._ts.GetColor(*Coord_TiaoZhan_Single)
            color_team = self._ts.GetColor(*Coord_TiaoZhan_Team)
            if self.__is_color_single():
                self._role = Role.Single
            elif color_team == Color_TiaoZhan_Ready or color_team == Color_TiaoZhan_Waiting:
                self._role = Role.Driver
            elif color_team == Color_TiaoZhan_Passenger:
                self._role = Role.Passenger
            current_time = time.clock()
            if current_time - start_time > 5:
                logging.info("Thread(%s) cannot judge role, so quit." % self.getName())
                self.__emit_stop_signal()

    def __main_loop(self):
        logging.debug("Thread(%s) is in the main loop as %s" % (self.getName(), str(self._role)))
        counter = 0
        while not self.is_stopped():
            counter += 1
            self.__enter_battlefield()

            # detect if we are in the battlefield
            while not self.__is_in_the_battle():
                self.__reject_xuan_shang()
                self.__sleep_or_quit(500)
            logging.debug("Thread(%s) in the battle" % self.getName())

            # detect if we finish the battle
            while self.__is_in_the_battle():
                self.__reject_xuan_shang()
                self.__sleep_or_quit(500)
            logging.debug("Thread(%s) battle finished" % self.getName())

            self.__bonus_received()
            self.__check_counter(counter)
            self.__sleep_or_quit(1000, 500)
            logging.debug("Thread(%s) restart to a new battle" % self.getName())
            self.__regroup_team()

    def __enter_battlefield(self):
        if self._role == Role.Single:
            while not self.__is_color_single():
                self.__reject_xuan_shang()
                self.__sleep_or_quit(500)
            click_in_region(self._ts, *Region_TiaoZhan_Single)
        elif self._role == Role.Driver:
            while True:
                self.__sleep_or_quit(500)
                self.__reject_xuan_shang()
                color = self._ts.GetColor(*Coord_TiaoZhan_Team)
                if color == Color_TiaoZhan_Waiting:
                    logging.debug("Thread(%s) waiting for passenger to join" % self.getName())
                elif color == Color_TiaoZhan_Ready:
                    click_in_region(self._ts, *Region_TiaoZhan_Driver)
                    break
        elif self._role == Role.Passenger:
            pass
        logging.debug("Thread(%s) already entered battlefield" % self.getName())

    def __bonus_received(self):
        if self._role == Role.Single:
            while not self.__is_color_single():
                self.__reject_xuan_shang()
                click_in_region(self._ts, *Region_Bonus)
                self.__sleep_or_quit(300, 300)
        elif self._role == Role.Driver or self._role == Role.Passenger:
            received = False
            while True:
                self.__reject_xuan_shang()
                color = self._ts.GetColor(*Coord_Finished)
                if color == Color_Finished or color == Color_Bonus:
                    received = True
                    click_in_region(self._ts, *Region_Bonus)
                    self.__sleep_or_quit(150, 150)
                elif received:
                    break

    def __regroup_team(self):
        if self._role == Role.Single:
            pass
        elif self._role == Role.Driver:
            while True:
                self.__reject_xuan_shang()
                color = self._ts.GetColor(*Coord_TiaoZhan_Team)
                if color == Color_TiaoZhan_Ready or color == Color_TiaoZhan_Waiting:
                    break
                color1 = self._ts.GetColor(*Coord_Driver_Invite_CheckButton)
                color2 = self._ts.GetColor(*Coord_Driver_Invite_OK)
                if color1 == Color_Driver_Invite_CheckButton_NO and color2 == Color_Driver_Invite_OK:
                    logging.debug("Thread(%s) invite passenger as driver" % self.getName())
                    click_in_region(self._ts, *Region_Driver_Invite_CheckButton)
                    self.__sleep_or_quit(500, 500)
                    click_in_region(self._ts, *Region_Driver_Invite_OK)
                    break
                self.__sleep_or_quit(500)
        elif self._role == Role.Passenger:
            while True:
                self.__reject_xuan_shang()
                color = self._ts.GetColor(*Coord_TiaoZhan_Team)
                if color == Color_TiaoZhan_Passenger or self.__is_in_the_battle():
                    break
                color1 = self._ts.GetColor(*Coord_Passenger_Accept1)
                color2 = self._ts.GetColor(*Coord_Passenger_Accept2)
                if color1 == color2 == Color_Passenger_Accept:
                    logging.debug("Thread(%s) accept the invitation as passenger" % self.getName())
                    click_in_region(self._ts, *Region_Passenger_Accept)
                    break

    def __is_color_single(self):
        color = self._ts.GetColor(*Coord_TiaoZhan_Single)
        return color == Color_TiaoZhan_Single or color == Color_TiaoZhan_Single2 or color == Color_TiaoZhan_Single3

    def __is_in_the_battle(self):
        return self._ts.GetColor(*Coord_InTheBattle) == Color_InTheBattle

    def __check_counter(self, counter):
        logging.debug("<--- Thread(%s) battle %d finished --->" % (self.getName(), counter))
        if self._count == counter:
            logging.info("<--- Thread(%s) %d/%d task done --->" % (self.getName(), counter, self._count))
            self.__emit_stop_signal()

    def __reject_xuan_shang(self):
        color = self._ts.GetColor(*Coord_XuanShang)
        if color == Color_XuanShang:
            logging.debug("received invitation XUAN-SHANG")
            self.__sleep_or_quit(650, 250)
            click_in_region(self._ts, *Region_XuanShang)
            logging.debug("successfully rejected XUAN-SHANG")
        self.__sleep_or_quit(50)

    def unbind_window(self):
        if self._ts is not None:
            logging.info('thread(%s) unBindWindow return: %d' % (self.getName(), self._ts.UnBindWindow()))
            self._ts = None

