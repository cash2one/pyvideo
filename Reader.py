import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import qdarkstyle


class Main(QMainWindow):
	def __init__(self):
		super().__init__()

		bar = self.menuBar()

		self.menu = bar.addMenu("菜单栏")



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon('./Source/app.png'))
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	mainMindow = Main()
	rect = QApplication.desktop().screenGeometry()
	mainMindow.resize(400, 700)
	mainMindow.setWindowTitle('阅读器')
	mainMindow.show()
	sys.exit(app.exec_())
