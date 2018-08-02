import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import requests
from bs4 import BeautifulSoup 
import dbfunc


class Home(QWidget):
    def __init__(self):
        super().__init__()
    
        self.initUI()

    def initUI(self):
        addTxBtn = QPushButton('添加腾讯用户', self)
        addTxBtn.move(20, 20)
        addTxBtn.clicked.connect(self.addTxClick)
        # self.addWidget(addTxBtn)
        
        # self.setGeometry(300, 300, 250, 150)
        # self.setWindowTitle('QCheckBox')
        # self.show()

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
    home.setGeometry(0, 0, 400, 300)
    home.setWindowTitle('kandian')
    home.show()
    sys.exit(app.exec_())
