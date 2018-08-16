from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import gfunc

class LocalVideo(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main = QVBoxLayout()
        self.setLayout(main)
        btn = QPushButton('videos文件')
        btn.clicked.connect(self.click)
        main.addWidget(btn)

        

    def click(self):
        
       dd = gfunc.getLocalFile('/Users/huangtao/Desktop/video')
