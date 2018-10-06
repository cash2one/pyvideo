from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import dbfunc
from MainAnchor import AnchorList
from config import *
from HTAddAnchor import AddAnchor
from MainVideos import VideosWidget
from Collect import tencent

class TencentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.anchors = dbfunc.getAnchor(PlatformType.tencent.value)
        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.anchorList = AnchorList('添加腾讯主播', self.anchors)
        self.anchorList.clicked_signal[int].connect(self.anchorRowAction)
        self.anchorList.addBtnClicked_signal.connect(self.addAnchorAction)
        self.anchorList.itemBtnClicked_signal[int].connect(self.anchorRowCollectionAction)
        self.anchorList.collectLatest_signal.connect(self.collectLatestAction)

        anchor = None
        if len(self.anchors) > 0 :
            anchor = self.anchors[0]
        self.videosWidget = VideosWidget(anchor)

        self.otherLayout = QVBoxLayout()
        self.renderOther()
        
        self.mainLayout.addWidget(self.anchorList)
        self.mainLayout.addWidget(self.videosWidget)
        self.mainLayout.addLayout(self.otherLayout)

        self.mainLayout.setStretchFactor(self.anchorList, 1)
        self.mainLayout.setStretchFactor(self.videosWidget, 5)
        self.mainLayout.setStretchFactor(self.otherLayout, 1)
        self.mainLayout.setContentsMargins(1,1,1,1)
        self.setLayout(self.mainLayout)

    def renderOther(self):
        self.updateVideoNumBtn = QPushButton('更新视频')
        self.updateVideoNumBtn.clicked.connect(self.updateVideoNumAction)
        self.showVideoNumLabel = QLabel()
        self.showVideoNumLabel.setWordWrap(True)
        self.otherLayout.addWidget(self.updateVideoNumBtn)
        self.otherLayout.addWidget(self.showVideoNumLabel)


    def updateVideoNumAction(self):
        anchors = dbfunc.getUploader(PlatformType.kandian.value)
        self.showVideoNumLabel.clear()
        text = ''
        for anchor in anchors:
            qq = anchor[1]
            res = dbfunc.getTodayWartpublishVideo(qq)
            res_all = dbfunc.getWartpublishVideo(qq)

            todayres = dbfunc.getTodayPublishedVideo(qq)
            text = text + qq+': \n        '+ str(len(todayres)) + ' -- ' + str(len(res)) + ' -- ' + str(len(res_all)) + '\n'
            # 刷新页面
            # QApplication.processEvents()

        print(text)
        self.showVideoNumLabel.setText(text)

    def addAnchorAction(self):
        self.addAnchor = AddAnchor()
        self.addAnchor.show()
        self.addAnchor.raise_()
        self.addAnchor.callback_sign[str].connect(self.addAnchorSuccess)

    def addAnchorSuccess(self, suc):
        if suc == 'success':
            # 刷新主播
            self.anchors =  dbfunc.getAnchor(PlatformType.tencent.value)
            print('刷新主播列表')
            QApplication.processEvents()
            self.anchorList.updateData(self.anchors)

    def anchorRowAction(self, row):
        aid = self.anchors[row][0]
        videos = dbfunc.getUnpublishedVideo(aid, [0, 13])
        
        self.videosWidget.anchor = self.anchors[row]
        self.videosWidget.updateListData(videos)

    # 采集
    def anchorRowCollectionAction(self, row):
        anchor = self.anchors[row]
        tencent.Tencent([anchor], CollectType.latest).start()

    # 采集最新视频
    def collectLatestAction(self):
        tc = tencent.Tencent().start()

    def updateUploader(self):
        self.videosWidget.updateUploaderBox()
        

