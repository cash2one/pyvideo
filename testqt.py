import sys
# TODO ModuleNotFoundError: No module named 'PyQt5.sip'
from PyQt5 import sip
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Ffmpeg(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(200, 100)
        self.show()

def main():
    app = QApplication(sys.argv)

    ex = Ffmpeg()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
    