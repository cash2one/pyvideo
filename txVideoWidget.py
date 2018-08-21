import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dbfunc

class TXVideoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.anchors = dbfunc.fetchAllAnchor()
        self.initUI()

    def initUI(self):

        self.mainHLayout = QHBoxLayout()
        self.leftVLayout = QVBoxLayout()
        self.rightVLayout = QVBoxLayout()

        self.setLayout(self.mainHLayout)
        self.mainHLayout.addLayout(self.leftVLayout)
        self.mainHLayout.addLayout(self.rightVLayout)

        self.mainHLayout.setStretchFactor(self.leftVLayout, 1)
        self.mainHLayout.setStretchFactor(self.rightVLayout, 5)

        self.addTxAnchorBtn = QPushButton('添加腾讯主播用户')
        self.addTxAnchorBtn.clicked.connect(self.addTxAnchorAction)
        self.txAnchorList = QListWidget()
        self.leftVLayout.addWidget(self.addTxAnchorBtn)
        self.leftVLayout.addWidget(self.txAnchorList)

        self.txAnchorList.addItems(['%s' % item[1] for item in self.anchors])
        self.txAnchorList.setCurrentRow(0)
        self.txAnchorList.clicked.connect(self.txAnchorAction)

        self.rightTopGridLayout = QGridLayout()
        self.videoList = QListWidget()
        self.videoList.addItems(["%s" % anchor[1] for anchor in self.anchors])

        self.rightBottomHLayout = QHBoxLayout()

        self.rightVLayout.addLayout(self.rightTopGridLayout)
        self.rightVLayout.addWidget(self.videoList)
        self.rightVLayout.addLayout(self.rightBottomHLayout)


    def addTxAnchorAction(self):
        pass

    def txAnchorAction(self):
        pass