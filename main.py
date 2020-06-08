# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from game_window import *
from game_control import *
from game_helper import *
import OnmyojiAssist


if __name__ == '__main__':
    init_logger()
    app = QApplication(sys.argv)
    assist = OnmyojiAssist.OnmyojiAssist()
    assist.show()
    app.setWindowIcon(QtGui.QIcon('yys.ico'))
    assist.setWindowIcon(QtGui.QIcon('yys.ico'))
    sys.exit(app.exec_())

    # hwnd_list = get_window_handlers()
    # dump_windows_information(hwnd_list)
    # for hwnd in hwnd_list:
    #     # pos = (IMG_XUAN_SHANG[0], IMG_XUAN_SHANG[1])
    #     # pos_end = (IMG_XUAN_SHANG[2], IMG_XUAN_SHANG[3])
    #
    #     img_file = './img/OVERFLOW.bmp'
    #     # img_src = screen_shot(hwnd_list[0])
    #     # show_img(img_src)
    #     maxVal, maxLoc = find_image(hwnd, img_file)
    #     print(maxVal, maxLoc)
    #     # pass

