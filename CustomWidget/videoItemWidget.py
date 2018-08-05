from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import requests
from CustomWidget import labelButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webview
import dbfunc

class VideoItemWidget(QWidget):
    """ a widget contains a picture and two line of text """
    def __init__(self, video):
        """
        :param title: str title
        :param subtitle: str subtitle
        :param icon_path: path of picture
        """
        super(VideoItemWidget, self).__init__()
        self.video = video
        title = video[2]
        subtitle = video[5]
        icon_path = ''
        qq = video[1]
        first_text = video[6]
        second_text = video[7]
        time = video[8]
        create_time = str(video[9])
        self.lb_title = QLabel(title)
        self.lb_title.setFont(QFont("Arial", 10, QFont.Bold))
        self.lb_title.setWordWrap(True)

        self.time = QLabel('腾讯发送日期：'+time)
        self.time.setFont(QFont("Arial", 10, QFont.StyleItalic))

        self.create_time = QLabel('收集日期: '+ create_time)
        self.create_time.setFont(QFont("Arial", 10, QFont.StyleItalic))


        self.lb_subtitle = QTextEdit(subtitle)
        self.lb_subtitle.setFont(QFont("Arial", 10, QFont.StyleItalic))
        # self.lb_subtitle.editingFinished.connect(self.editingFinished)

        self.lb_icon = labelButton.LabelButton()
        # self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(160, 90)
        self.lb_icon.clicked.connect(self.playClick)
        # self.playbtn = QPushButton('播放')
        # self.playbtn.move()
        # self.lb_icon.setWidget(self.playbtn)

        self.qq = QLineEdit(qq)
        self.qq.editingFinished.connect(self.editingFinished)

        self.first_class = QLineEdit(first_text)
        self.first_class.editingFinished.connect(self.editingFinished)
        self.second_class = QLineEdit(second_text)
        self.second_class.editingFinished.connect(self.editingFinished)


        url = video[13] 
        if url is None:
            url = 'https://puui.qpic.cn/vpic/0/r0745f7blex_160_90_3.jpg/0'
        
        req = requests.get(url)

        pixMap = QPixmap()
        pixMap.loadFromData(req.content)
        # pixMap.scaled(80, 80)
        # pixMap = QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(pixMap)
        self.double_click_fun = None
        self.init_ui()
    
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

        
        # self.video[6] = text

    def text_edited(self):
        print('edit '+self.first_class.text())

    def init_ui(self):
        """handle layout"""
        ly_main = QVBoxLayout()
        ly_right = QVBoxLayout()
        ly_right.addWidget(self.lb_title)
        ly_right.addWidget(self.time)

        ly_right.addWidget(self.create_time)

        ly_right.addWidget(self.lb_subtitle)

        ly_right.addWidget(self.qq)

        ly_right.addWidget(self.first_class)
        ly_right.addWidget(self.second_class)

        ly_right.setAlignment(Qt.AlignVCenter)
        ly_main.addWidget(self.lb_icon)
        ly_main.addLayout(ly_right)
        self.setLayout(ly_main)
        # self.resize(130, 100)


    def playClick(self):
        print('1111')
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