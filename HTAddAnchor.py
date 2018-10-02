from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import requests
from config import *
from bs4 import BeautifulSoup 
import dbfunc
import gfunc
import re

class AddAnchor(QWidget):

    callback_sign = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self):
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.nameLab = QLabel('主播链接或UIN：')
        self.nameLine = QLineEdit()
        self.btn = QPushButton('添  加')
        self.btn.clicked.connect(self.btnAction)

        self.mainLayout.addWidget(self.nameLab, 0, 0)
        self.mainLayout.addWidget(self.nameLine, 0, 1)
        self.mainLayout.addWidget(self.btn, 1, 0, 1, 3)


        self.resize(300, 200)
        self.setWindowTitle('添加腾讯主播用户')

    def btnAction(self):
        name = self.nameLine.text()

        if len(name) == 0:
            QMessageBox.warning(self, '', "请输入腾讯主播链接或UIN", QMessageBox.Yes)
            return

        # url http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos

        # 1 查找uin
        uin = ''
        url = ''
        if name.find('vplus') == -1:
            uin = name
            url = VPlusBaseUrl+name
        else:
            url = name
            name = name.replace('/videos', '')
            uin = name.replace('http://v.qq.com/vplus/', '')
        uin = uin.strip()
        # 2 验证数据库是否存在 uin
        if len(uin) < 20:
            QMessageBox.warning(self, '', '请正确填写腾讯主播链接', QMessageBox.Yes) 
            return
        # 3 验证数据库中是否存在 uin platform fromUserId
        dd = {
            'uin': uin,
            'platform': PlatformType.tencent.value,
            'fromUserId': gfunc.getUserId()
        }
        isExist = dbfunc.checkAnchor(dd)
        if isExist:
            QMessageBox.warning(self, '', "该主播已存在，不需再添加", QMessageBox.Yes)   
            return

        res = requests.get(name, headers=Headers)
        # TODO html编码问题 用content
        text = res.content
        soup = BeautifulSoup(text, 'html.parser')
        nickname = str(soup.find('span', attrs={'id': 'userInfoNick'}).get_text())
        intr = soup.find('div', attrs={'class': 'intro_txt'}).find(attrs={'class': 'txt'}).get_text()

        user_count = soup.find('ul', attrs={'class': 'user_count'}).find_all('span', attrs={'class': 'num'})
        vnum = user_count[1].get_text() 
        dic = {
            'name': nickname,
            'uin': uin,
            'intr': intr,
            'vnum': vnum,
            'platform': PlatformType.tencent.value
        }

        flag = dbfunc.addAnchor(dic)
        print(flag)
        if flag:
            button = QMessageBox.information(self, nickname, "添加成功", QMessageBox.Yes)
            if button:
                self.close()
                self.callback_sign.emit('success')
        else:
            QMessageBox.warning(self,
                                nickname,
                                "添加失败",  
                                QMessageBox.Yes) 





