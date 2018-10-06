import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dbfunc
from config import *
from CustomWidget import userWidget, consoleWidget
from HTUpload import Upload
from MainLocal import LocalWidget
from global_data import global_data, updateUploaderPlatform, updateUploaderArray

class UploadWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.platforms = UploadPlatformData
        
        updateUploaderPlatform(self.platforms[0]['platform'])

        self.setUI()
        # 上传 使用线程
        self.upload = Upload()

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
        self.account.currentIndexChanged.connect(self.changedAccountAction)
        self.consoleWidget = consoleWidget.MyConsole()

        self.uploadBtn = QPushButton('上传')
        self.uploadBtn.clicked.connect(self.uploadAction)

        self.uploadCurrentBtn = QPushButton('当前上传')
        self.uploadCurrentBtn.clicked.connect(self.uploadCurrentAction)

        self.mainLayout.addWidget(self.platform)
        self.mainLayout.addWidget(self.addBtn)
        self.mainLayout.addWidget(self.account)
        self.mainLayout.addWidget(self.uploadBtn)
        self.mainLayout.addWidget(self.uploadCurrentBtn)
        # self.mainLayout.addWidget(self.consoleWidget)


        self.setLayout(self.mainLayout)

    def _setAccount(self):
        self.account.addItems(["%s" % uploader[1] for uploader in global_data.UploaderArray])

    def _setPlatform(self):
        self.platform.addItems([item['name'] for item in self.platforms])


    def addBtnClick(self):
        index = self.platform.currentIndex()
        self.user = userWidget.UserWidget(self.platforms[index])
        self.user.callback_sign[str].connect(self.callbackSuccess)

        self.user.show()
        self.user.raise_()

    def callbackSuccess(self, platform):
        updateUploaderArray()
        self.account.clear()
        self._setAccount()

    def changedPlatform(self):
        index = self.platform.currentIndex()
        updateUploaderPlatform(self.platforms[index]['platform'])
        self.account.clear()
        self._setAccount()

    def changedAccountAction(self):
        # index = self.account.currentIndex()
        # selectUploader = global_data.UploaderArray[index]
        pass

    # 上传
    def uploadAction(self):
        # data = LocalWidget().getData()
        index = self.account.currentIndex()
        selectUploader = global_data.UploaderArray[index]
        print(selectUploader)
        self.upload.run(global_data.UploaderPlatform, uploaders=[selectUploader])

    def uploadCurrentAction(self):
        data = []

        index = self.account.currentIndex()
        selectUploader = global_data.UploaderArray[index]
        name = selectUploader[1]
        videos = global_data.Videos
        print(videos)
        for video in videos:
            publish_time = video[10]

            qq = video[1]
            if qq == name and publish_time is None:
                data.append(video)

        self.upload.run(global_data.UploaderPlatform, uploaders=[selectUploader], data=data)
