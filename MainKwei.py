from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import dbfunc
from MainAnchor import AnchorList
from config import *

class KweiWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.anchors = dbfunc.getAnchor(KuaishouPlatform)
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.anchorList = AnchorList('添加快手主播', self.anchors)
        self.mainLayout.addWidget(self.anchorList)
        self.setLayout(self.mainLayout)

        self.anchorList.clicked_signal[int].connect(self.anchorRowAction)
        self.anchorList.addBtnClicked_signal.connect(self.addAnchorAction)
        self.anchorList.itemBtnClicked_signal[int].connect(self.anchorRowCollectionAction)

    def addAnchorAction(self):
        pass

    def anchorRowAction(self, row):
        print(row)

    def anchorRowCollectionAction(self, row):
        pass
