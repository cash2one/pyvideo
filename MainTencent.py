from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import dbfunc
from MainAnchor import AnchorList
from config import *
from HTAddAnchor import AddAnchor
from MainVideos import VideosWidget
import qq

class TencentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.anchors = dbfunc.getAnchorFromPlatform(TencentPlatform)
        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.anchorList = AnchorList('添加腾讯主播', self.anchors)
        self.anchorList.clicked_signal[int].connect(self.anchorRowAction)
        self.anchorList.addBtnClicked_signal.connect(self.addAnchorAction)
        self.anchorList.itemBtnClicked_signal[int].connect(self.anchorRowCollectionAction)

        self.videosWidget = VideosWidget()

        
        self.mainLayout.addWidget(self.anchorList)
        self.mainLayout.addWidget(self.videosWidget)

        self.mainLayout.setStretchFactor(self.anchorList, 1)
        self.mainLayout.setStretchFactor(self.videosWidget, 5)

        self.setLayout(self.mainLayout)

    def addAnchorAction(self):
        self.addAnchor = AddAnchor()
        self.addAnchor.show()
        self.addAnchor.raise_()
        self.addAnchor.callback_sign[str].connect(self.addAnchorSuccess)

    def addAnchorSuccess(self, suc):
        if suc == 'success':
            # 刷新主播
            self.anchors =  dbfunc.getAnchorFromPlatform(TencentPlatform)
            print('刷新主播列表')
            QApplication.processEvents()
            self.anchorList.updateData(self.anchors)

    def anchorRowAction(self, row):
        aid = self.anchors[row][0]
        videos = dbfunc.getNotPublishVideoFromAid(aid, [0, 13])
        self.videosWidget.updateListData(videos)

    # 采集
    def anchorRowCollectionAction(self, row):
        anchor = self.anchors[row]
        qq.main([anchor], 'all')
        

