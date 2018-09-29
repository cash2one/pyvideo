import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dbfunc
from config import *
from CustomWidget import userWidget, consoleWidget
from HTUpload import Upload
from MainLocal import LocalWidget

class UploadWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.platforms = UploadPlatformData
        self.selectPlatfrom = self.platforms[0]['platform']
        self.uploaders = dbfunc.getUploader(self.selectPlatfrom)
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

        self.uploadBtn = QPushButton('上传')
        self.uploadBtn.clicked.connect(self.uploadAction)

        self.mainLayout.addWidget(self.platform)
        self.mainLayout.addWidget(self.addBtn)
        self.mainLayout.addWidget(self.account)
        self.mainLayout.addWidget(self.uploadBtn)
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
        self.uploaders = dbfunc.getUploader(platform)
        self.account.clear()
        self._setAccount()

    def changedPlatform(self):
        index = self.platform.currentIndex()
        self.selectPlatfrom = self.platforms[index]['platform']
        self.uploaders = dbfunc.getUploader(self.selectPlatfrom)
        self.account.clear()
        self._setAccount()

    # 上传
    def uploadAction(self):
        data = LocalWidget().getData()
        print(data)
        upload = Upload(self.selectPlatfrom, data)
        upload.run()
