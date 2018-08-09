import os
import time
# from splinter import Browser

import test01

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import gfunc
from Source import ddd 


class Test(QWidget):
    def __init__(self):
        super().__init__()

        testw = QLabel('11' ,self)

        tt = ddd.main()

        # res = gfunc.participle('甜蜜暴击的什么啊')

        # dd = test01.home()
        # print(dd)
        testw.setText(tt)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    home = Test()
    home.setGeometry(0, 0, 200, 200)
    home.setWindowTitle('kandian')
    home.show()
    
    sys.exit(app.exec_())


# with Browser('chrome', executable_path='./chromedriver', headless=False) as browser:
#     url = 'http://www.baidu.com'
#     browser.visit(url)
#     time.sleep(10)