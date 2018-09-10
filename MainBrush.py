from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
# import loggor
import myglobalmodule
import test04

class MainBrush(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi()
        self.resize(200, 100)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def setupUi(self):
        btn = QPushButton('btn', self)
        btn.clicked.connect(self.btnAction)

        
    def btnAction(self):
        loggor.info('MainBrush')
        test04.run()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    bb = MainBrush()
    bb.show()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()