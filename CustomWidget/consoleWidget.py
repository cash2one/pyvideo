import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import time

class EmittingStream(QtCore.QObject):
        textWritten = QtCore.pyqtSignal(str)
        def write(self, text):
            self.textWritten.emit(str(text))

class MyConsole(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        # 重定向输出
        # sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        # sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)
    
    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


    def normalOutputWritten(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
        QApplication.processEvents()

def main():
    app = QApplication(sys.argv)
    cons = MyConsole()
    cons.resize(100, 100)
    cons.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()