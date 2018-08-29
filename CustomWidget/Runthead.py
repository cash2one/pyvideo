
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import *
import time

# 继承QThread
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal()
 
    def __init__(self, parent=None):
        super(Runthread, self).__init__()
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self._signal.emit();
 
