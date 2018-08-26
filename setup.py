#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO ModuleNotFoundError: No module named 'PyQt5.sip'

from PyInstaller.__main__ import run

# -F:打包成一个EXE文件 
# -w:不带console输出控制台，window窗体格式 
# --paths：依赖包路径 
# --icon：图标 
# --noupx：不用upx压缩 
# --clean：清理掉临时文件

if __name__ == '__main__':
    opts = [ 
            '-D', '-w',
            '-p=C:\\Users\\Administrator\\Desktop\\pyvideo\\Source',
            '-p=C:\\Users\\Administrator\\Desktop\\pyvideo\\CustomWidget',
            '-p=C:\\Users\\Administrator\\Desktop\\pyvideo\\DBHelper\\dbHelper.py',
            '--noupx', '--clean',
            'MainWindow.py'
            ]

    run(opts)