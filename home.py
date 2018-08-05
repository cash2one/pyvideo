import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests
from bs4 import BeautifulSoup 
import dbfunc
import kandian
import qq
from CustomWidget import videoItemWidget

class Home(QWidget):
    def __init__(self):
        super().__init__()
    
        self.kdusers = dbfunc.fetchAllUser()
        self.anchors = dbfunc.fetchAllAnchor()
        self.videos = dbfunc.fetchVideoFromAnchor(1)
        self.initUI()

    def initUI(self):

        conHBoxLayout = QHBoxLayout()
        self.setLayout(conHBoxLayout)
        leftVBoxLayout = QVBoxLayout()
        rightVBoxLayout = QVBoxLayout()
        centerVBoxLayout = QVBoxLayout()
        
        conHBoxLayout.addLayout(leftVBoxLayout)
        conHBoxLayout.addLayout(centerVBoxLayout)
        conHBoxLayout.addLayout(rightVBoxLayout)
        conHBoxLayout.setStretchFactor(leftVBoxLayout, 1)
        conHBoxLayout.setStretchFactor(centerVBoxLayout, 3)
        conHBoxLayout.setStretchFactor(rightVBoxLayout, 1)

        # 左边
        addTxBtn = QPushButton('添加腾讯用户')
        addTxBtn.clicked.connect(self.addTxClick)

        leftVBoxLayout.addWidget(addTxBtn)

        self.leftListWidget = QListWidget()
        leftVBoxLayout.addWidget(self.leftListWidget)
        self.leftListWidget.addItems(["%s" % anchor[1] for anchor in self.anchors])
        self.leftListWidget.setCurrentRow(0)
        self.leftListWidget.clicked.connect(self.currentChanged)
        # 中间
        # 

        centerTopHLayout = QHBoxLayout()
        centerVBoxLayout.addLayout(centerTopHLayout)

        collectCurrentBtn = QPushButton('采集当前视频')
        collectCurrentBtn.clicked.connect(self.collectCurrentClick)
        collectAllBtn = QPushButton('采集腾讯视频')
        collectAllBtn.clicked.connect(self.collectAllClick)

        updateCurrentBtn = QPushButton('更新当前')
        updateCurrentBtn.clicked.connect(self.updateCurrentClick)

        centerTopHLayout.addWidget(collectCurrentBtn)
        centerTopHLayout.addWidget(collectAllBtn)
        centerTopHLayout.addWidget(updateCurrentBtn)

        self.centerListWidget = QListWidget()
        centerVBoxLayout.addWidget(self.centerListWidget)
        self.centerListWidget.setViewMode(QListView.IconMode)
        self.centerListWidget.setFlow(QListView.LeftToRight)
        # self.centerListWidget.addItems(['%s' % video[2] for video in self.videos])
        for video in self.videos:
            self._setItem(video)

        # 右边
        self.combBox = QComboBox()
        self.combBox.addItems(["%s" % user[1] for user in self.kdusers])
        rightVBoxLayout.addWidget(self.combBox)

        qqBtn = QPushButton('开始行动')
        qqBtn.clicked.connect(self.startKandianClick)
        rightVBoxLayout.addWidget(qqBtn)


        # self.addWidget(addTxBtn)
        
        # self.setGeometry(300, 300, 250, 150)
        # self.setWindowTitle('QCheckBox')
        # self.show()
    def _setItem(self, video):
        item_widget = QListWidgetItem()
        # 必须设置这个 大小才显示
        item_widget.setSizeHint(QSize(200, 350))
        self.centerListWidget.addItem(item_widget)

        videoWidget = videoItemWidget.VideoItemWidget(video)
        self.centerListWidget.setItemWidget(item_widget, videoWidget)  

    def currentChanged(self):
        index = self.leftListWidget.currentRow()

        aid = self.anchors[index][0]
        res = dbfunc.fetchVideoFromAnchor(aid)
        print(len(res))
        self.centerListWidget.clear()

        self.videos = res
        for video in self.videos:
            self._setItem(video)
        # self.centerListWidget.clear()
        # self.centerListWidget.repaint()

    def collectCurrentClick(self):

        qq.main([self.anchors[index]])

    def collectAllClick(self):
        qq.main()

    def updateCurrentClick(self):
        self.currentChanged()
    
    def startKandianClick(self):
        index = self.combBox.currentIndex()
        name = self.kdusers[index][1]
        pwd = self.kdusers[index][2]
        kandian.login(name, pwd)
        # print(str(index))

    def addTxClick(self):
        value, ok = QInputDialog.getText(self, "添加腾讯用户", "请输入文本uin:", QLineEdit.Normal, "")

        if ok:
            if len(value) == 0:
                reply = QMessageBox.warning(self,
                                    "提示",  
                                    "请输入腾讯uin！",  
                                    QMessageBox.Yes | QMessageBox.No)
            else:
                # 添加 先查找腾讯
                # http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos
                headers = {
                    'user_agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                }
                url = 'http://v.qq.com/vplus/%s/videos' % value
                res = requests.get(url, headers=headers)
                # TODO html 编码 操蛋
                text = res.content
                soup = BeautifulSoup(text, 'html.parser')
                name = str(soup.find('span', attrs={'id': 'userInfoNick'}).get_text())
                intr = soup.find('div', attrs={'class': 'intro_txt'}).find(attrs={'class': 'txt'}).get_text()

                user_count = soup.find('ul', attrs={'class': 'user_count'}).find_all('span', attrs={'class': 'num'})
                vnum = user_count[1].get_text()

                flag = dbfunc.insertAnchor(name, value, intr, vnum)
                if flag:
                    QMessageBox.information(self, 
                                    '',
                                    "添加成功",  
                                    QMessageBox.Yes)
                else:
                    QMessageBox.warning(self,
                                '',
                                "添加失败",  
                                QMessageBox.Yes) 
               

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    home = Home()
    home.setGeometry(0, 0, 1200, 700)
    home.setWindowTitle('kandian')
    home.show()
    
    sys.exit(app.exec_())
