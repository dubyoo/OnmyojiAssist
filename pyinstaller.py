# -*- coding: utf-8 -*-
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['main.py', '-F', '-w', '--icon=yys.ico']
    run(opts)
