# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import OnmyojiAssist
from MyHelper import *


if __name__ == '__main__':
    # 需要提前在 windows 中注册 TSPlug.dll
    # 方法: regsvr32.exe TSPlug.dll

    init_logger()

    app = QApplication(sys.argv)
    assist = OnmyojiAssist.OnmyojiAssist()
    assist.show()
    sys.exit(app.exec_())

