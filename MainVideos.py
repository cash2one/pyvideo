from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from config import *
from CustomWidget import videoItemWidget
import dbfunc
import time
from HTQThread import HTQThread

class VideosWidget(QWidget):
    def __init__(self):
        super().__init__()

        
        '''
            video 状态
            1.已发布 账号来查询 今天和昨天的数量 4--10
            2.未发布 今天 以前 填写了所属账号（待发布）以账号查询 
            未填写 分了类 未分类 下载了和未下载
        '''

        self.videoStatus = VideoStatus
        self.videos = dbfunc.getVideos()
        self.uploaders = dbfunc.getUploader(KandianPlatform)

        self.setUI()
        self.setTopUI()
        self.setListWidget()

    
    def setUI(self):
        self.mainLayout = QVBoxLayout()

        self.topLayout = QGridLayout()
        self.topLayout.setAlignment(Qt.AlignLeft)
        self.listWidget = QListWidget()
        # self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setFlow(QListView.LeftToRight)
        self.listWidget.setWrapping(True)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.listWidget)
        self.setLayout(self.mainLayout)

    def setTopUI(self):
        self.statusLab = QLabel('发布状态:')
        self.statusBox = QComboBox()
        self.statusBox.addItems(self.videoStatus)
        self.statusBox.currentIndexChanged.connect(self.statusChanged)
        self.uploaderLab = QLabel(' 上传账号:')
        self.uploaderBox = QComboBox()
        self.uploaderBox.addItems('%s' % item[1] for item in self.uploaders)
        self.uploaderBox.currentIndexChanged.connect(self.uploaderChanged)

        self.topLayout.addWidget(self.statusLab, 0, 0)
        self.topLayout.addWidget(self.statusBox, 0, 1)
        self.topLayout.addWidget(self.uploaderLab, 0, 2)
        self.topLayout.addWidget(self.uploaderBox, 0, 3)

    def setListWidget(self):

        self.thread = HTQThread()
        self.thread.signal.connect(self.setList)
        self.thread.start()


    def setList(self):

        self.listWidget.addItem(QListWidgetItem())
        self.listWidget.clear()
        QApplication.processEvents()

        for video in self.videos:
            self._setItem(video)

    def _setItem(self, video):

        item_widget = QListWidgetItem()
        # 必须设置这个 大小才显示
        item_widget.setSizeHint(QSize(210, 305))
        self.listWidget.addItem(item_widget)

        videoWidget = videoItemWidget.VideoItem(video, self.uploaders)
        self.listWidget.setItemWidget(item_widget, videoWidget)  

    def updateListData(self, videos):
        self.videos = videos
        self.setListWidget()

    def statusChanged(self):
        pass
    def uploaderChanged(self):
        pass
    

