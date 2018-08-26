from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import gfunc

class AnchorList(QWidget):

    clicked_signal = pyqtSignal(int)
    addBtnClicked_signal = pyqtSignal()
    itemBtnClicked_signal = pyqtSignal(int)
    # data [[aid, name, uin, intr, vnum, page, fromUserId, fromPlatform], []]
    def __init__(self, btnTitle='', data=[]):
        super().__init__()
        self.data = data
        self.clickedItemBtn = self.itemBtnAction
        self.btnTitle = btnTitle
        self.initUI()

    def initUI(self):
        
        self.mainLayout = QVBoxLayout()
        self.addBtn = QPushButton(self.btnTitle)
        self.addBtn.clicked.connect(self.addBtnAction)
        self.listWidget = QListWidget()
        self.listWidget.setCurrentRow(0)
        self.listWidget.clicked.connect(self.clickedAction)

        for index in range(0, len(self.data)):
            item = self.data[index]
            self._setItem(item, index)
        

        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.addBtn)
        self.mainLayout.addWidget(self.listWidget)

    def _renderItem(self, item, index):
        itemWidget = QWidget()
        hLayout = QHBoxLayout()
        lab = QLabel(item[1])
        btn = QPushButton('采集')
        btn.clicked.connect(lambda: self.itemBtnAction(index))
        hLayout.addWidget(lab)
        hLayout.addWidget(btn)
        itemWidget.setLayout(hLayout)
        return itemWidget

    def itemBtnAction(self, index):
        if self.itemBtnClicked_signal:
            self.itemBtnClicked_signal.emit(index)

    def _setItem(self, item, index):
        item_widget = QListWidgetItem()
        item_widget.setSizeHint(QSize(100, 50))
        self.listWidget.addItem(item_widget)

        aItem = self._renderItem(item, index)
        self.listWidget.setItemWidget(item_widget, aItem)
   
    def updateData(self, data):
        self.listWidget.clear()
        self.data = data
        for index in range(0, len(self.data)):
            item = self.data[index]
            self._setItem(item, index)

    def clickedAction(self):
        row = self.listWidget.currentRow()
        if self.clicked_signal:
            self.clicked_signal.emit(int(row))

    def addBtnAction(self):
        if self.addBtnClicked_signal:
            self.addBtnClicked_signal.emit()