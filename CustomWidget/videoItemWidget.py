from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import requests
from CustomWidget import labelButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webview
import dbfunc
import gfunc

class VideoItem(QWidget):
    """ a widget contains a picture and two line of text """
    def __init__(self, video, qqs, callback):
        """
        :param title: str title
        :param subtitle: str subtitle
        :param icon_path: path of picture
        """
        super().__init__()
        self.callback = callback
        self.video = video
        title = video[2]
        tags = video[5]
        icon_path = ''
        qq = video[1]
        first_text = video[6]
        second_text = video[7]
        time = video[8]
        create_time = str(video[9])
        finish_time = str(video[10])

        self.lb_title = QTextEdit(title)
        self.lb_title.setFont(QFont("Arial", 10, QFont.Bold))
        self.lb_title.textChanged.connect(self.titleChanged)

        # self.lb_title.setWordWrap(True)

        self.time = QLabel('腾讯发送日期：'+time)
        self.time.setFont(QFont("Arial", 10, QFont.StyleItalic))

        self.create_time = QLabel('收集日期: '+ create_time)
        self.create_time.setFont(QFont("Arial", 10, QFont.StyleItalic))

        self.finish_time = QLabel('完成日期: '+ finish_time)
        self.finish_time.setFont(QFont("Arial", 10, QFont.StyleItalic))

        # tags
        self.lb_subtitle = QTextEdit(tags)
        self.lb_subtitle.setFont(QFont("Arial", 10, QFont.StyleItalic))
        self.lb_subtitle.textChanged.connect(self.tagsEdit)

        self.lb_icon = labelButton.LabelButton()
        # self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(160, 90)
        self.lb_icon.clicked.connect(self.playClick)
        # self.playbtn = QPushButton('播放')
        # self.playbtn.move()
        # self.lb_icon.setWidget(self.playbtn)


        self.qqbox = QComboBox()
        if len(qq) > 0 and finish_time != 'None' :
            self.qqbox.addItem(qq)
            self.qqbox.setEditable(False)
        
        else:
            qqArr = ['']
            index = 0
            for i in range(0, len(qqs)):
                item = qqs[i][1]
                qqArr.append(item)
                if item == qq:
                    index = i+1
            self.qqbox.addItems(qqArr)
            self.qqbox.setEditable(False)

            self.qqbox.setCurrentIndex(index)

        self.qqbox.currentIndexChanged.connect(self.qqclick)

        self.data = gfunc.readJsonFile('classify')
        firstArr = self.data['first']

        self.first_class = QComboBox()
        self.first_class.addItems(["%s" % first for first in firstArr])
        firstIndex = 0
        if len(first_text) > 0:
            for i in range(0, len(firstArr)):
                if first_text == firstArr[i]:
                    firstIndex = i
        if firstIndex == 0:
            self.first_class.setEditable(True) 
        else:
            self.first_class.setEditable(False) 

        self.first_class.setCurrentIndex(firstIndex)
        self.first_class.currentIndexChanged.connect(self.firstclick)
        

        secondArr = self.data['second']
        self.second_class = QComboBox()
        self.second_class.addItems(["%s" % item for item in secondArr])
        secondIndex = 0
        if len(second_text) > 0:
            for i in range(0, len(secondArr)):
                if second_text == secondArr[i]:
                    secondIndex = i 
        if secondIndex == 0:
            self.second_class.setEditable(True) 
        else:
            self.second_class.setEditable(False)       
        self.second_class.setCurrentIndex(secondIndex)
        self.second_class.currentIndexChanged.connect(self.secondclick)
        

        url = video[13] 
        if url is None:
            url = 'http://puui.qpic.cn/vpic/0/r0745f7blex_160_90_3.jpg/0'
        
        req = requests.get(url)

        pixMap = QPixmap()
        pixMap.loadFromData(req.content)
        # pixMap.scaled(80, 80)
        # pixMap = QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(pixMap)
        self.double_click_fun = None
        self.init_ui()

    
    def qqclick(self):
        qq = self.qqbox.currentText()
        dbfunc.updateVideoQQ(self.video[0], qq)

    def titleChanged(self):
        title = self.lb_title.toPlainText()
        dic = { 'title': title }
        self._updateVideo(dic)

    def _updateVideo(self, dic):
        dbfunc.updateVideo(self.video[0], dic, 'videos')

    # 更新tags
    def tagsEdit(self):
        text = self.lb_subtitle.toPlainText()
        dic = {'tags': text}
        self._updateVideo(dic)

    def firstclick(self):
        firstText = self.first_class.currentText()
        index = self.first_class.currentIndex()
        if index == 0:
            self.first_class.setEditable(True)
        else:
            self.first_class.setEditable(False)
        dic = {'first_class': firstText}
        dbfunc.updateVideoFromData(self.video[0], dic, 'videos')
        self.writeClassify('first', firstText)

    # mode first second string
    def writeClassify(self, mode, text):   
        # 去掉前后空格 rstrip 后空格
        text = text.strip()     
        flag = False

        itemArr = self.data[mode]
        for item in itemArr:
            if item == text:
                flag = True
        if flag == False:
            # 新增
            itemArr.append(text)
            self.data[mode] = itemArr
            print(self.data)
            gfunc.writeJsonFile(self.data, 'classify')
                
        
    def secondclick(self):
        secondText = self.second_class.currentText()
        index = self.second_class.currentIndex()
        if index == 0:
            self.second_class.setEditable(True)
        else:
            self.second_class.setEditable(False)
        dic = {'second_class': secondText}
        dbfunc.updateVideoFromData(self.video[0], dic, 'videos')
        self.writeClassify('second', secondText)


    def editingFinished(self):
        # 编辑完成 更新数据库
        firsttext = self.first_class.text()
        secondtext = self.second_class.text()
        tags = self.lb_subtitle.toPlainText()
        qq = self.qq.text()
        dic = {}
        if len(firsttext) > 0:
            dic['first_class'] = firsttext
        if len(secondtext) > 0:
            dic['second_class'] = secondtext 
        if len(qq) > 0:
            dic['qq'] = qq
        if len(tags) > 0:
            dic['tags'] = tags  
        print(dic)
        dbfunc.updateVideo(self.video[0], dic, 'videos')

    def init_ui(self):
        """handle layout"""
        ly_main = QVBoxLayout()
        ly_right = QVBoxLayout()
        ly_right.addWidget(self.lb_title)
        ly_right.addWidget(self.time)

        ly_right.addWidget(self.create_time)
        ly_right.addWidget(self.finish_time)

        ly_right.addWidget(self.lb_subtitle)

        ly_right.addWidget(self.qqbox)

        ly_h_class = QHBoxLayout()
        ly_h_class.addWidget(self.first_class)
        ly_h_class.addWidget(self.second_class)
        ly_right.addLayout(ly_h_class)

        ly_right.setAlignment(Qt.AlignVCenter)
        ly_main.addWidget(self.lb_icon)
        ly_main.addLayout(ly_right)
        self.setLayout(ly_main)
        # self.resize(130, 100)


    def playClick(self):
        self.callback(self.video[3])
        # app = QApplication([])
        # view = QWebEngineView()
        # view.load(QUrl("http://www.baidu.com"))
        # view.show()
        # app.exec_()
        # screen = webview.Form()
        # screen.show()
        # url = "https://www.baidu.com"
        # screen.load(url)

    def get_lb_title(self):
        return self.lb_title.text()

    def get_lb_subtitle(self):
        return self.lb_subtitle.text()