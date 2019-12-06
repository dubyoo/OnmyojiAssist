# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import OnmyojiAssist
from MyHelper import *


if __name__ == '__main__':
    # 需要提前在 windows 中注册 TSPlug.dll
    # 方法: regsvr32.exe TSPlug.dll

    handler = MyQtHandler()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG, handlers=[handler])
    # logging.debug('python version: %s' % sys.version)

    app = QApplication(sys.argv)
    assist = OnmyojiAssist.OnmyojiAssist()
    assist.show()
    sys.exit(app.exec_())

