from MyHelper import *
from enum import Enum, unique
import threading


@unique
class Role(Enum):
    Unknown = 0
    Single = 1
    Driver = 2
    Passenger = 3


class QuitThread(Exception):
    pass


class OnmyojiThread(threading.Thread):
    def __init__(self, onmyoji_assist, ts_plugin):
        super(OnmyojiThread, self).__init__()
        self._stop_event = threading.Event()
        self._onmyoji_assist = onmyoji_assist
        self._ts = ts_plugin
        self._role = Role.Unknown
        self._stop_after_finish = False
        self._count = 0

    def set_count(self, count):
        self._count = count

    def set_stop_after_finish(self):
        self._stop_after_finish = True

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self):
        logger.info("线程(%s) 开始运行" % self.getName())
        try:
            self.__role_judgement()
            self.__main_loop()
        except QuitThread as e:
            logger.info("线程(%s) 已退出" % self.getName())

    def __test_loop(self):
        counter = 0
        while not self.is_stopped():
            counter += 1
            logger.info('Thread(%s) count %d' % (self.getName(), counter))
            self.__sleep_or_quit(500, 2000)
            logger.debug('Thread(%s) count %d  1' % (self.getName(), counter))
            self.__check_counter(counter)
            self.__sleep_or_quit(1000)
            logger.debug('Thread(%s) count %d  2' % (self.getName(), counter))
            self.__sleep_or_quit(1000)
            logger.debug('Thread(%s) count %d  3' % (self.getName(), counter))

    def __emit_stop_signal(self):
        self.stop()
        self._onmyoji_assist.stop_signal.emit(int(self.getName()))

    def __sleep_or_quit(self, sleep_time, variable_time=0):
        if not self.is_stopped():
            random_sleep(sleep_time, variable_time)
        if self.is_stopped():
            logger.debug("线程(%s) 即将停止" % self.getName())
            raise QuitThread('quit')

    def __role_judgement(self):
        self._role = Role.Unknown
        start_time = time.clock()
        while self._role == Role.Unknown:
            self.__sleep_or_quit(500)
            self.__reject_xuan_shang()
            color_team = self._ts.GetColor(*Coord_TiaoZhan_Team)
            if self.__is_color_single():
                self._role = Role.Single
            elif color_team == Color_TiaoZhan_Ready or color_team == Color_TiaoZhan_Waiting:
                self._role = Role.Driver
            elif color_team == Color_TiaoZhan_Passenger:
                self._role = Role.Passenger
            current_time = time.clock()
            if current_time - start_time > 10:
                logger.info("线程(%s) 无法识别角色，正在退出" % self.getName())
                self.__emit_stop_signal()

    def __main_loop(self):
        logger.info("线程(%s) 主循环开始，识别出角色：%s" % (self.getName(), str(self._role)))
        counter = 0
        while not self.is_stopped():
            counter += 1
            self.__enter_battlefield()

            # detect if we are in the battlefield
            while not self.__is_in_the_battle():
                self.__reject_xuan_shang()
                self.__sleep_or_quit(500)
            logger.debug("线程(%s) 已经进入战场" % self.getName())

            # detect if we finish the battle
            while self.__is_in_the_battle():
                self.__reject_xuan_shang()
                self.__sleep_or_quit(500)
            logger.debug("线程(%s) 战斗结束" % self.getName())

            self.__bonus_received()
            self.__check_counter(counter)
            self.__sleep_or_quit(1000, 500)
            logger.debug("线程(%s) 准备进入下一轮" % self.getName())
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
                    logger.debug("线程(%s) 等待队友加入" % self.getName())
                elif color == Color_TiaoZhan_Ready:
                    click_in_region(self._ts, *Region_TiaoZhan_Driver)
                    break
        elif self._role == Role.Passenger:
            pass
        logger.debug("线程(%s) 正在进入战场" % self.getName())

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
                    logger.debug("线程(%s) 自动邀请队友" % self.getName())
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
                    logger.debug("线程(%s) 自动接收组队邀请" % self.getName())
                    click_in_region(self._ts, *Region_Passenger_Accept)
                    break

    def __is_color_single(self):
        color = self._ts.GetColor(*Coord_TiaoZhan_Single)
        return color == Color_TiaoZhan_Single or color == Color_TiaoZhan_Single2 or color == Color_TiaoZhan_Single3

    def __is_in_the_battle(self):
        return self._ts.GetColor(*Coord_InTheBattle) == Color_InTheBattle

    def __check_counter(self, counter):
        logger.info("<--- 线程(%s) 第 %d 次战斗结束 --->" % (self.getName(), counter))
        if self._count == counter or self._stop_after_finish:
            logger.info("<--- 线程(%s) 计划任务 %d/%d 完成 --->" % (self.getName(), counter, self._count))
            self.__emit_stop_signal()

    def __reject_xuan_shang(self):
        color = self._ts.GetColor(*Coord_XuanShang)
        if color == Color_XuanShang:
            logger.info("线程(%s) 检测到悬赏邀请" % self.getName())
            self.__sleep_or_quit(650, 250)
            click_in_region(self._ts, *Region_XuanShang)
            logger.info("线程(%s) 已拒绝悬赏" % self.getName())
        self.__sleep_or_quit(50)

    def unbind_window(self):
        if self._ts is not None:
            logger.info('Thread(%s) unBindWindow return: %d' % (self.getName(), self._ts.UnBindWindow()))
            self._ts = None

