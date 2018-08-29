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
import re
import subprocess


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
        self.url = self.video[3]
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
        

        pic = video[13] 
        if pic is None:
            pic = 'http://puui.qpic.cn/vpic/0/r0745f7blex_160_90_3.jpg/0'
        pixMap = QPixmap()
        try:
            req = requests.get(pic)
            pixMap.loadFromData(req.content)
        except Exception as e:
            pass
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
        ly_top = QHBoxLayout()
        ly_top_right = QVBoxLayout()
        ly_right = QVBoxLayout()
        ly_right.addWidget(self.lb_title)
        ly_right.addWidget(self.time)

        ly_right.addWidget(self.create_time)
        ly_right.addWidget(self.finish_time)

        ly_right.addWidget(self.lb_subtitle)

        ly_right.addWidget(self.qqbox)
        self.qqbox.setFixedHeight(22)
        self.qqbox.setFont(QFont("Arial", 12, QFont.StyleItalic))

        ly_h_class = QHBoxLayout()
        ly_h_class.addWidget(self.first_class)
        ly_h_class.addWidget(self.second_class)

        self.first_class.setFixedHeight(24)
        self.first_class.setFont(QFont("Arial", 12, QFont.StyleItalic))
        self.second_class.setFixedHeight(24)
        self.second_class.setFont(QFont("Arial", 12, QFont.StyleItalic))

        ly_right.addLayout(ly_h_class)

        ly_right.setSpacing(2)
        ly_main.fillWidth = True
        # ly_main.addWidget(self.lb_icon)
        is_exist_local = self.video[14]
        text = 'D'
        if str(is_exist_local) == '1':
            text = 'E'
        self.downBtn = QPushButton(text)
        if str(is_exist_local) == '1':
            self.downBtn.setEnabled(False)
        else:
            self.downBtn.setEnabled(True)

        self.downBtn.clicked.connect(self.downClick)

        ly_top_right.addWidget(self.downBtn)

        if str(is_exist_local) == '1':
            self.playbtn = QPushButton('P')
            self.playbtn.clicked.connect(self.playbtnClick)
            ly_top_right.addWidget(self.playbtn)

            self.qubtn = QPushButton('Q')
            self.qubtn.clicked.connect(self.qubtnClick)
            ly_top_right.addWidget(self.qubtn)


        ly_top.addWidget(self.lb_icon)
        ly_top.addLayout(ly_top_right)

        ly_main.addLayout(ly_top)
        ly_main.addLayout(ly_right)
        self.setLayout(ly_main)
        # self.resize(130, 100)

    def qubtnClick(self):
        # 去水印
        infile = self.video[15]
        outfile =  self.video[15].replace('.mp4', '_new.mp4')
        # 960
        x = '690'
        y = '30'
        w = '135'
        h = '40'
        strcmd = ['ffmpeg -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h +' '+outfile]
        result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)

        if gfunc.isfile(outfile):
            print('存入去水印的视频')
            dic = {
                'local_path': outfile
            }
            dbfunc.updateVideoFromData(self.video[0], dic, 'videos')


    def playbtnClick(self):
        paggname = self.video[15]
        # 960
        x = '690'
        y = '30'
        w = '135'
        h = '40'
        # ffplay -i infile/v0769lodrau.mp4 -vf delogo=x=10:y=10:w=195:h=55:show=1
        strcmd = ['ffplay -i ' +paggname+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h+':show=1']
        result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)

    # 下载
    def downClick(self):
        base = 'http://192.168.1.23/qq.php?url='
        url = base+self.url
        print(url)

        gfunc.createDir('videos')

        res = requests.get(url)
        text = res.text
        url = re.findall("http:.*", text)[0]
        print(url)
        self.writeFile(url)

    def writeFile(self, url):
        urlArr = url.split('/')
        filename = ''
        for item in urlArr:
            if item.find('mp4') != -1:
                print(item)
                filename = item.split('?')[0]        

        filename = 'videos/'+filename
        print(filename)
        isfile = gfunc.isfile(filename)
        if isfile == False:

            res = requests.get(url)
            data = res.content
            with open(filename, "wb") as code:
                code.write(data)

            print('视频写入文件成功')
        else:
            print('视频已经下载')

        # 存入数据库
        print('存入数据库')
        dic = {
            'is_exist_local': '1',
            'local_path': filename
        }
        dbfunc.updateVideoFromData(self.video[0], dic, 'videos')
        # 处理水印


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