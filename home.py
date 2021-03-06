import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtSvg import QSvgWidget

import qdarkstyle
import requests
from bs4 import BeautifulSoup 
import dbfunc
import gfunc
import kandian
import qq
from CustomWidget import videoItemWidget, consoleWidget, userWidget, Runthread
import time
import webview
import txvideo
import localVideo
import douyinWidget
from txVideoWidget import TXVideoWidget
from Collect import tencent
from config import *


class Home(QWidget):
    def __init__(self):
        super().__init__()
    
        self.kdusers = dbfunc.fetchAllUser()
        self.anchors = dbfunc.fetchAllAnchor()
        aid = '0'
        if len(self.anchors) > 0:
            aid = self.anchors[0][0]
        print(aid)
        self.videos = dbfunc.fetchVideoFromAnchor(aid)
        self.initUI()
        self.userwidget = userWidget.UserWidget(self.userWidgetCallback)

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
        hbox = QHBoxLayout()

        addKandianBtn = QPushButton('添加看点用户')
        addKandianBtn.clicked.connect(self.addKandianClick)

        self.combBox = QComboBox()
        self.combBox.addItems(["%s" % user[1] for user in self.kdusers])

        qqBtn = QPushButton('今天')
        qqBtn.clicked.connect(self.startKandianClick)

        currentBtn = QPushButton('当前')
        currentBtn.clicked.connect(self.currentKandianClick)

        allBtn = QPushButton('所有账号')
        allBtn.clicked.connect(self.allbtnClick)
        kdCollectBtn = QPushButton('看点采集')
        kdCollectBtn.clicked.connect(self.kdCollectAction)

        self.consoleWidget = consoleWidget.MyConsole()
        self.rightVBoxLayout.addWidget(addKandianBtn)
        self.rightVBoxLayout.addWidget(self.combBox)
        self.rightVBoxLayout.addLayout(hbox)

        hbox.addWidget(qqBtn)
        hbox.addWidget(currentBtn)
        self.rightVBoxLayout.addWidget(allBtn)
        self.rightVBoxLayout.addWidget(kdCollectBtn)


        self.rightVBoxLayout.addWidget(self.consoleWidget)

    def centerUI(self):
        self.centerVBoxLayout = QVBoxLayout()
        self.localVideo = TXVideoWidget()
        self.txVideo = QWidget()
        self.douyinVideo = douyinWidget.Douyin()
        self.tabWidget = QTabWidget()

        self.tabWidget.addTab(self.txVideo, '腾讯视频')
        self.tabWidget.addTab(self.douyinVideo, '抖音视频')
        self.tabWidget.addTab(self.localVideo, '本地视频')
        self.txHLayout = QHBoxLayout()
        self.txVideo.setLayout(self.txHLayout)
        self.txHLayout.addLayout(self.leftVBoxLayout)
        self.txHLayout.addLayout(self.centerVBoxLayout)
        self.txHLayout.setStretchFactor(self.leftVBoxLayout, 1)
        self.txHLayout.setStretchFactor(self.centerVBoxLayout, 5)

        centerTopHLayout = QGridLayout()
        self.centerVBoxLayout.addLayout(centerTopHLayout)

        collectCurrentBtn = QPushButton('采集当前视频')
        collectCurrentBtn.clicked.connect(self.collectCurrentClick)
        collectAllBtn = QPushButton('采集一页腾讯视频')
        collectAllBtn.clicked.connect(self.collectAllClick)

        updateCurrentBtn = QPushButton('更新当前')
        updateCurrentBtn.clicked.connect(self.updateCurrentClick)

        todayVideoBtn = QPushButton('今天视频')
        todayVideoBtn.clicked.connect(self.todayVideoClick)

        notPubAllVideoBtn = QPushButton('下载视频并去水印')
        notPubAllVideoBtn.clicked.connect(self.notPubAllVideoClick)

        showVideoNumBtn = QPushButton('展示今天账号视频数量')
        showVideoNumBtn.clicked.connect(self.showVideoNumClick)
        self.showVideoNumLabel = QLabel()
        self.showVideoNumLabel.setWordWrap(True)

        currentVideoNumBtn = QPushButton('展示当前账号视频数量')
        currentVideoNumBtn.clicked.connect(self.currentVideoNumClick)

        self.currentVideoNumLabel = QLabel()
        self.currentVideoNumLabel.setWordWrap(True)

        centerTopHLayout.addWidget(collectCurrentBtn, 0, 0)
        centerTopHLayout.addWidget(collectAllBtn, 0, 1)
        centerTopHLayout.addWidget(updateCurrentBtn, 0, 2)
        centerTopHLayout.addWidget(todayVideoBtn, 0, 3)
        centerTopHLayout.addWidget(notPubAllVideoBtn, 0, 4)
        centerTopHLayout.addWidget(showVideoNumBtn, 1, 0)
        centerTopHLayout.addWidget(self.showVideoNumLabel, 1, 1, 1, 4)
        centerTopHLayout.addWidget(currentVideoNumBtn, 2, 0)
        centerTopHLayout.addWidget(self.currentVideoNumLabel, 2, 1, 2, 4)

        self.centerListWidget = QListWidget()
        self.centerVBoxLayout.addWidget(self.centerListWidget)
        self.centerListWidget.setViewMode(QListView.IconMode)
        self.centerListWidget.setFlow(QListView.LeftToRight)
        # self.centerListWidget.verticalScrollBar().actionTriggered.connect(self.onActionTriggered)

        # self.centerListWidget.addItems(['%s' % video[2] for video in self.videos])
        self.updateListWedget()

        # self.loadWidget = QSvgWidget(minimumHeight=60, minimumWidth=60, visible=False)
        # # self.centerVBoxLayout.addWidget(self.loadWidget)
        # self.loadWidget.load(Svg_icon_loading)

        self.centerBottomHLayout = QHBoxLayout()
        self.centerBottomHLayout.setAlignment(Qt.AlignCenter)
        self.centerVBoxLayout.addLayout(self.centerBottomHLayout)
        # self.loadWidget.setVisible(True)

    # def resizeEvent(self, event):
    #     super(Home, self).resizeEvent(event)
    #     self.loadWidget.setGeometry(
    #         10,
    #         10,
    #         self.loadWidget.minimumWidth(),
    #         self.loadWidget.minimumHeight()
    #     )

    # def onActionTriggered(self, action):
    #     # 这里要判断action=QAbstractSlider.SliderMove，可以避免窗口大小改变的问题
    #     # 同时防止多次加载同一个url
    #     if action != QAbstractSlider.SliderMove:
    #         return
    #     # 使用sliderPosition获取值可以同时满足鼠标滑动和拖动判断
    #     if self.centerListWidget.verticalScrollBar().sliderPosition() == self.centerListWidget.verticalScrollBar().maximum():
    #         # 可以下一页了
    #         self.load()

    # def load(self):
        # self.loadWidget.setVisible(True)
        # QTimer.singleShot(5000, self._load)

    # def _load(self):
        # self.loadWidget.setVisible(False)


    def addPage(self):
        self.allpage = 11
        self.pageBtnArr = []
        self.maxpage = 12
        if self.allpage >= 11:
           self.maxpage = 12
        else:
            self.maxpage = self.allpage+2

        for i in range(0, self.maxpage):
            pbtn = QPushButton(str(i+1))
            pbtn.setCheckable(False)
            pbtn.setFixedSize(QSize(32, 26))
            pbtn.clicked.connect(self.pageAction)
            self.pageBtnArr.append(pbtn)
            self.centerBottomHLayout.addWidget(pbtn)
            if i == 0:
                pbtn.setText('1')
            elif i == self.maxpage-1:
                pbtn.setText(str(self.allpage))
            elif  i == 1:
                pbtn.setText('...')
                pbtn.hide()
            elif i == self.maxpage-2:
                pbtn.setText('...')
                if self.allpage > 10:
                    pbtn.show()
                else:
                    pbtn.hide()
            else:
                pbtn.setText(str(i))

        # for i in range(0, len(self.pageBtnArr)):
        #     btn = self.pageBtnArr[i]
        #     btn.setText(str(page-3+i))
            
    def pageAction(self):
        text = self.sender().text()
        if text == '...':
            return
        page = int(text)
        print(page)
        btnLen = len(self.pageBtnArr)
        # 左4右5
        if self.allpage > 10:
            if 10-page < 4:
                self.pageBtnArr[1].show()
            elif 10-page >=4:
                self.pageBtnArr[1].hide()
            elif self.allpage-page>7:
                self.pageBtnArr[btnLen-2].show()
            elif self.allpage-page<=7:
                self.pageBtnArr[btnLen-2].hide()
            else:
                for i in range(2, btnLen-2):
                    self.pageBtnArr[i].setText(str(page-5+i))

    

    def callback(self, url):
        print(url)
        self.web = webview.Form()
        self.web.load(url)

        # streamArr = txvideo.jiexi_tx(url)
        # if len(streamArr) > 0:
        #     streamurl = streamArr[0]['urls'][0]
        #     print(streamurl)

        #     self.web.load(streamurl)
            # self.downvideo(streamurl)

    def downvideo(self, url):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36"}
        res = requests.get(url, headers=header)
        video = res.content

        file = url.split('/')[-1]
        print('url: '+ url)
        with open(file, "wb") as f:
            f.write(video)


    def _setItem(self, video):
        QApplication.processEvents()

        item_widget = QListWidgetItem()
        # 必须设置这个 大小才显示
        item_widget.setSizeHint(QSize(210, 305))
        self.centerListWidget.addItem(item_widget)

        videoWidget = videoItemWidget.VideoItem(video, self.kdusers, self.callback)
        self.centerListWidget.setItemWidget(item_widget, videoWidget)  

    def addUI(self):
        self.setLayout(self.boxLayout)

        # self.boxLayout.addLayout(self.leftVBoxLayout)
        # self.boxLayout.addLayout(self.centerVBoxLayout)
        self.boxLayout.addWidget(self.tabWidget)
        self.boxLayout.addLayout(self.rightVBoxLayout)
        # 横向比例布局 1: 3: 1
        # self.boxLayout.setStretchFactor(self.leftVBoxLayout, 1)
        self.boxLayout.setStretchFactor(self.tabWidget, 4)
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
            res_all = dbfunc.fetchVideo(qq)

            todayres = dbfunc.fetchTodayPublishedVideo(qq)
            text = text + qq+': '+ str(len(todayres)) + ' -- ' + str(len(res)) + ' -- ' + str(len(res_all)) + ' '
            # 刷新页面
            # QApplication.processEvents()

        print(text)
        self.showVideoNumLabel.setText(text)            

    # 下载视频并去水印
    def notPubAllVideoClick(self):
        # res = dbfunc.fetchNotPublishedAndQQ()
        # self.videos = res
        # self.updateListWedget()

        self.thread = Runthread.Runthread()
        self.thread._signal.connect(self.callbacklog)
        self.thread.start()

    def callbacklog(self):
        res = dbfunc.fetchTodayWartPublishVideo()

        for item in res:
            is_exist_local = item[14]
            local_path = item[15]
            url = item[3]
            idd = item[0]
            print(str(idd)+' :  '+local_path)
            if gfunc.isfile(local_path) == False:
                # 1. 下载
                local_path = gfunc.downVideo(url)
                print(local_path)
                # 2. 存入数据库
                print('存入数据库')
                is_exist_local = '1'
                dic = {
                    'is_exist_local': is_exist_local,
                    'local_path': local_path
                }
                dbfunc.updateVideoFromData(idd, dic, 'videos')
            
            # 2.去水印
            outfile = gfunc.watermarks(local_path)

            print('存入去水印的视频')
            if outfile:
                dic = { 'local_path': outfile }
                dbfunc.updateVideoFromData(item[0], dic, 'videos')
            time.sleep(1)
        print('下载完成去水印完成')

    # 展示当前腾讯视频数量
    def currentVideoNumClick(self):
        anchors=dbfunc.fetchAllUser()
        qqdic = {}
        for item in anchors:
            qq = item[1]
            qqdic[qq] = 0

        for video in self.videos:
            qq = video[1]
            qq = qq.strip() # 去掉前后空格
            if len(qq) > 0:
                qqdic[qq] = qqdic[qq] + 1
        text = ''
        qqkeys = qqdic.keys()
        for item in qqkeys:
            text = text + item + ': '+str(qqdic[item]) + '    '
        print(text)
        self.currentVideoNumLabel.setText(text)
            
    # 更新选中腾讯用户
    def currentChanged(self):
        index = self.leftListWidget.currentRow()
        # todo 
        if len(self.anchors) > 0:
            
            aid = self.anchors[index][0]

            print('更新腾讯主播：'+ self.anchors[index][1])

            res = dbfunc.fetchVideoFromAnchor(aid)
            self.videos = res

            self.updateListWedget()

    
    # 更新list videos
    def updateListWedget(self):
        self.updateList()

    def updateList(self):
        self.listthread = Runthread.Runthread()
        self.listthread._signal.connect(self.runUpdateList)
        self.listthread.start()

    
    def runUpdateList(self):
        # self.loadWidget.setVisible(False)

        print('更新列表：'+str(len(self.videos)))
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
        print('采集当前主播所有视频')
        index = self.leftListWidget.currentRow()
        print(index)
        self.collectVideo([self.anchors[index]], page='all')

    # 采集腾讯视频
    def collectAllClick(self):
        print('开始采集腾讯视频')
        self.collectVideo()
        print('采集结束')
    
    def collectVideo(self, anchors=None, page=None):
        qq.main(anchors, page)
        # self.cthread = Runthread.Runthread()
        # self.cthread._signal.connect(lambda:self.runcollect(anchors, page))
        # self.cthread.start()
        # tencent.Tencent(anchors, page)


    def runcollect(self, anchors=None, page=None):
        tencent.Tencent(anchors, page)

    # 更新当前 videos
    def updateCurrentClick(self):
        self.currentChanged()

    # 上传看点

    def uploadKandian(self, name=None, pwd=None, data=None):
        # self.uthread = Runthread.Runthread()
        # self.uthread._signal.connect(lambda:self.runupload(name, pwd, data))
        # self.uthread.start()
        self.runupload(name, pwd, data)

    def runupload(self, name, pwd, data):
        if name == None:
            for item in self.kdusers:
                kandian.login(item[1], item[2])
                time.sleep(5)
        else:
            kandian.login(name, pwd, data)

    def allbtnClick(self):
        self.uploadKandian()

    # 上传看点 今天的
    def startKandianClick(self):
        index = self.combBox.currentIndex()
        name = self.kdusers[index][1]
        pwd = self.kdusers[index][2]
        self.uploadKandian(name, pwd)

    # 当前页选中的
    def currentKandianClick(self):
        data = []
        index = self.combBox.currentIndex()
        name = self.kdusers[index][1]
        pwd = self.kdusers[index][2]

        for video in self.videos:
            publish_time = video[10]

            qq = video[1]
            if qq == name and publish_time is None:
                data.append(video)
        self.uploadKandian(name, pwd, data)

    # 看点采集 需登录看点或者拿到cookes
    def kdCollectAction(self):
        brush.main()
        
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
    
    def addKandianClick(self):
        self.userwidget.show()
        self.userwidget.raise_()

    def userWidgetCallback(self, name):
        # 添加成功看点账号更新
        self.anchors = dbfunc.fetchAllAnchor()
        self.combBox.addItem(name)

# if __name__ == '__main__':
    
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("./Source/app.png"))

#     app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

#     home = Home()
#     rect = QApplication.desktop().screenGeometry()
#     home.resize(rect.width(), rect.height())
#     home.setWindowTitle('看点自动测试')
#     home.show()
    
#     sys.exit(app.exec_())
