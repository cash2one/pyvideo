
from PyQt5.QtWidgets import *
from MainTencent import TencentWidget
from MainKwei import KweiWidget
from MainUpload import UploadWidget
from MainLocal import LocalWidget

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.mainLayout = QHBoxLayout()

        self.tab = QTabWidget()
        self.upload = UploadWidget()

        self.tencent = TencentWidget()
        self.kwei = KweiWidget()
        self.local = LocalWidget()
        self.tab.addTab(self.tencent, '腾讯视频')
        self.tab.addTab(self.kwei, '快手视频')
        self.tab.addTab(self.local, '本地视频')

        self.mainLayout.addWidget(self.tab)
        self.mainLayout.addWidget(self.upload)
        # 比例布局
        self.mainLayout.setStretchFactor(self.tab, 5)
        self.mainLayout.setStretchFactor(self.upload, 1)

        self.setLayout(self.mainLayout)
