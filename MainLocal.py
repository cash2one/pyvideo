import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import dbfunc
import gfunc
from config import *
import re

class LocalWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.tableModel = None
        self.tableView = None
        self.setUpUI()

    def impDatabaseAction(self):
        pass
        bb = self.tableModel.rowCount()
        pp = self.tableModel.columnCount()
        print(bb)
        print(pp)
        bb = self.tableModel.invisibleRootItem()
        print(bb)
    def setTopView(self):
        self.impDatabase = QPushButton('导入数据库')
        self.impDatabase.clicked.connect(self.impDatabaseAction)
        self.topLayout.addWidget(self.impDatabase)

    def setUpUI(self):

        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.layout.addLayout(self.topLayout)
        self.setTopView()
        # tableview
        self.tableView = QTableView()

        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        headerList = ['acount', 'path','title', 'dec', 'class', 'tag', 'publish']
        self.tableModel = QStandardItemModel()
        self.tableModel.setHorizontalHeaderLabels(headerList)
        dirname = 'Local' 
        files = gfunc.getLocalFile(dirname)
        print(files)

        if files:
            row = len(files)

            for r,data in enumerate(files):
                # title 替换 [剧集编号] 视频格式.mp4
                title = data.replace('.mp4', '')
                nm = re.findall(r'\[.*\]', title)
                if len(nm) > 0:
                    title = title.replace(nm[0], '') 

                path = dirname+'/'+data
                for c,cell in enumerate(headerList):
                    it = QStandardItem(str(cell))
                    if cell == 'title' or cell == 'dec':

                        it = QStandardItem(title)
                        it.setEditable(True)

                    if cell == 'path':
                        it = QStandardItem(path)
                        it.setEditable(False)

                    if cell == 'class':
                        # 分类 多个用空格隔开
                        clas = gfunc.classFromTitle(title)
                        value = ''
                        if len(clas[0]) > 0:
                            value = clas[0]+' '+clas[1]
                        it = QStandardItem(value)
                    if cell == 'tag':
                        seg_list = gfunc.participle(title)
                        tags = ' '.join(seg_list)
                        it = QStandardItem(tags)
                    
                    self.tableModel.setItem(r, c, it)


        self.tableView.setModel(self.tableModel)

        self.layout.addWidget(self.tableView)

        self.setLayout(self.layout)

    def getData(self):
        row = self.tableModel.rowCount()
        column = self.tableModel.columnCount()
        arr = []
        for i in range(0, row):
            dic = {}
            # for j in range(0, column):
            dic['account'] = self.tableModel.item(i, 0).text()
            dic['path'] = self.tableModel.item(i, 1).text()
            dic['title'] = self.tableModel.item(i, 2).text()
            dic['dec'] = self.tableModel.item(i, 3).text()
            dic['class'] = self.tableModel.item(i, 4).text()
            dic['tag'] = self.tableModel.item(i, 5).text()
            arr.append(dic)
        return arr





