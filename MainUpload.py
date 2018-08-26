import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dbfunc
from config import *
from CustomWidget import userWidget, consoleWidget

class UploadWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.platforms = [
                    {'name': '看点', 'platform': KandianPlatform},
                    {'name': '企鹅号', 'platform': QierhaoPlatform},
                ]
        self.uploaders = dbfunc.getUploaderWithPlatform(self.platforms[0]['platform'])
        self.setUI()

    def setUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.platform = QComboBox()
        self._setPlatform()
        self.platform.currentIndexChanged.connect(self.changedPlatform)

        self.addBtn = QPushButton('添加用户')
        self.addBtn.clicked.connect(self.addBtnClick)

        self.account = QComboBox()
        self._setAccount()
        self.consoleWidget = consoleWidget.MyConsole()


        self.mainLayout.addWidget(self.platform)
        self.mainLayout.addWidget(self.addBtn)
        self.mainLayout.addWidget(self.account)
        # self.mainLayout.addWidget(self.consoleWidget)


        self.setLayout(self.mainLayout)

    def _setAccount(self):
        self.account.addItems(["%s" % uploader[1] for uploader in self.uploaders])

    def _setPlatform(self):
        self.platform.addItems([item['name'] for item in self.platforms])


    def addBtnClick(self):
        index = self.platform.currentIndex()
        self.user = userWidget.UserWidget(self.platforms[index])
        self.user.callback_sign[str].connect(self.callbackSuccess)

        self.user.show()
        self.user.raise_()


    def callbackSuccess(self, platform):
        self.uploaders = dbfunc.getUploaderWithPlatform(platform)
        self.account.clear()
        self._setAccount()

    def changedPlatform(self):
        index = self.platform.currentIndex()
        self.uploaders = dbfunc.getUploaderWithPlatform(self.platforms[index]['platform'])
        self.account.clear()
        self._setAccount()
