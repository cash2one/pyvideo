import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

import requests
from bs4 import BeautifulSoup 
import dbfunc
import kandian
import qq
from CustomWidget import videoItemWidget
from CustomWidget import consoleWidget
import time


class Home(QWidget):
    def __init__(self):
        super().__init__()
    
        self.kdusers = dbfunc.fetchAllUser()
        self.anchors = dbfunc.fetchAllAnchor()
        self.videos = dbfunc.fetchVideoFromAnchor(1)
        self.initUI()

    def leftUI(self):
        self.leftVBoxLayout = QVBoxLayout()

        addTxBtn = QPushButton('添加腾讯用户')
        addTxBtn.clicked.connect(self.addTxClick)

        self.leftListWidget = QListWidget()
        self.leftListWidget.addItems(["%s" % anchor[1] for anchor in self.anchors])
        self.leftListWidget.setCurrentRow(0)
        self.leftListWidget.clicked.connect(self.currentChanged)

        self.leftVBoxLayout.addWidget(addTxBtn)
        self.leftVBoxLayout.addWidget(self.leftListWidget)



    def rightUI(self):
        self.rightVBoxLayout = QVBoxLayout()

        self.combBox = QComboBox()
        self.combBox.addItems(["%s" % user[1] for user in self.kdusers])

        qqBtn = QPushButton('开始行动')
        qqBtn.clicked.connect(self.startKandianClick)

        self.consoleWidget = consoleWidget.MyConsole()
                
        self.rightVBoxLayout.addWidget(self.combBox)
        self.rightVBoxLayout.addWidget(qqBtn)
        self.rightVBoxLayout.addWidget(self.consoleWidget)

    def centerUI(self):
        self.centerVBoxLayout = QVBoxLayout()

        centerTopHLayout = QGridLayout()
        self.centerVBoxLayout.addLayout(centerTopHLayout)

        collectCurrentBtn = QPushButton('采集当前视频')
        collectCurrentBtn.clicked.connect(self.collectCurrentClick)
        collectAllBtn = QPushButton('采集腾讯视频')
        collectAllBtn.clicked.connect(self.collectAllClick)

        updateCurrentBtn = QPushButton('更新当前')
        updateCurrentBtn.clicked.connect(self.updateCurrentClick)

        todayVideoBtn = QPushButton('今天的视频')
        todayVideoBtn.clicked.connect(self.todayVideoClick)

        showVideoNumBtn = QPushButton('展示今天账号视频数量')
        showVideoNumBtn.clicked.connect(self.showVideoNumClick)

        self.showVideoNumLabel = QLabel()
        self.showVideoNumLabel.setWordWrap(True)

        centerTopHLayout.addWidget(collectCurrentBtn, 0, 0)
        centerTopHLayout.addWidget(collectAllBtn, 0, 1)
        centerTopHLayout.addWidget(updateCurrentBtn, 0, 2)
        centerTopHLayout.addWidget(todayVideoBtn, 0, 3)

        centerTopHLayout.addWidget(showVideoNumBtn, 1, 0)
        centerTopHLayout.addWidget(self.showVideoNumLabel, 1, 1, 1, 3)

        self.centerListWidget = QListWidget()
        self.centerVBoxLayout.addWidget(self.centerListWidget)
        self.centerListWidget.setViewMode(QListView.IconMode)
        self.centerListWidget.setFlow(QListView.LeftToRight)
        # self.centerListWidget.addItems(['%s' % video[2] for video in self.videos])
        for video in self.videos:
            self._setItem(video)

    def _setItem(self, video):
        QApplication.processEvents()

        item_widget = QListWidgetItem()
        # 必须设置这个 大小才显示
        item_widget.setSizeHint(QSize(220, 350))
        self.centerListWidget.addItem(item_widget)

        videoWidget = videoItemWidget.VideoItem(video, self.kdusers)
        self.centerListWidget.setItemWidget(item_widget, videoWidget)  

        QApplication.processEvents()

    def addUI(self):
        self.setLayout(self.boxLayout)

        self.boxLayout.addLayout(self.leftVBoxLayout)
        self.boxLayout.addLayout(self.centerVBoxLayout)
        self.boxLayout.addLayout(self.rightVBoxLayout)
        # 横向比例布局 1: 3: 1
        self.boxLayout.setStretchFactor(self.leftVBoxLayout, 1)
        self.boxLayout.setStretchFactor(self.centerVBoxLayout, 3)
        self.boxLayout.setStretchFactor(self.rightVBoxLayout, 1)

    def initUI(self):
        self.boxLayout = QHBoxLayout()
        self.setLayout(self.boxLayout)
        self.leftUI()
        self.centerUI()
        self.rightUI()

        self.addUI()

    # 展示今天账号视频数量
    def showVideoNumClick(self):
        anchors=dbfunc.fetchAllUser()
        self.showVideoNumLabel.clear()
        text = ''
        for anchor in anchors:
            qq = anchor[1]
            res = dbfunc.fetchVideo(qq, 'today')
            todayres = dbfunc.fetchTodayPublishedVideo(qq)
            text = text + qq+': '+ str(len(todayres)) + ' -- ' + str(len(res)) + ' '
            # 刷新页面
            # QApplication.processEvents()

        print(text)
        self.showVideoNumLabel.setText(text)

    # 更新选中腾讯用户
    def currentChanged(self):
        index = self.leftListWidget.currentRow()
        aid = self.anchors[index][0]

        print('更新腾讯主播：'+ self.anchors[index][1])

        res = dbfunc.fetchVideoFromAnchor(aid)
        print(self.anchors[index][1] + ' 总共视频数量: '+ str(len(res)))
        self.centerListWidget.clear()

        self.videos = res
        for video in self.videos:
            self._setItem(video)
        # self.centerListWidget.clear()
        # self.centerListWidget.repaint()
    
    # 更新list videos
    def updateListWedget(self):
        print('更新 列表')
        self.centerListWidget.clear()
        for video in self.videos:
            self._setItem(video)
        print('刷新结束')

    # 今天添加的视频
    def todayVideoClick(self):
        print('获取今天采集的视频')
        self.videos = dbfunc.fetchTodayVideo()
        self.updateListWedget()

    # 采集当前主播的视频
    def collectCurrentClick(self):
        index = self.combBox.currentIndex()
        qq.main([self.anchors[index]])

    # 采集腾讯视频
    def collectAllClick(self):
        print('开始采集腾讯视频')

        qq.main()

        print('采集结束')

    def callbackCollectAllVideo(self):
        qq.main()

    # 更新当前 videos
    def updateCurrentClick(self):
        self.currentChanged()
    
    # 开始上传看点
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
