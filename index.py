import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import subprocess
import os

class Index(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initUi()
    
    def initUi(self):
        movie = QMovie('王者歪传：好爸爸?坏爸爸?王者荣耀里的塑料父子情.mp4')
        movie.setBackgroundColor(QColor('red'))
        lab = QLabel(self)
        lab.setFixedSize(200, 200)
        lab.setMovie(movie)
        movie.start()
        # self.setWidget(lab)

    def setupUi(self):
        self.resize(300, 300)
        self.move(100, 100)
        self.setWindowTitle('111')
        self.show()

def main():
    app = QApplication(sys.argv)
    index = Index()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
