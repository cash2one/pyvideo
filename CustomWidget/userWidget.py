from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import dbfunc
from config import *

class UserWidget(QWidget):

    callback_sign = pyqtSignal(str)

    def __init__(self, platformItem):
        super().__init__()
        self.platformItem = platformItem
        self.initUI()

    def initUI(self):

        mainLayout = QGridLayout()

        nameLab = QLabel('账号：')
        pwdLab = QLabel('密码：')

        self.name = QLineEdit()
        self.pwd = QLineEdit()

        extLab = QLabel('别名：')
        self.ext = QLineEdit()

        btn = QPushButton('添加')
        btn.clicked.connect(self.btnClick)

        self.setLayout(mainLayout)
        mainLayout.addWidget(nameLab, 0, 0)
        mainLayout.addWidget(self.name, 0, 1)
        mainLayout.addWidget(pwdLab, 1, 0)
        mainLayout.addWidget(self.pwd, 1, 1)
        mainLayout.addWidget(extLab, 2, 0)
        mainLayout.addWidget(self.ext, 2, 1)

        mainLayout.addWidget(btn, 3, 0, 3, 3)

        self.resize(300, 200)
        self.setWindowTitle('添加%s用户' % self.platformItem['name'])
        # self.show()

    def btnClick(self):
        name = self.name.text()
        pwd = self.pwd.text()
        ext = self.ext.text()

        if len(name) == 0 or len(pwd) == 0:
            QMessageBox.warning(self, '', "请输入账号和密码", QMessageBox.Yes)
            return
        platform = self.platformItem['platform']
        # 登陆方式 qq email
        loginType = LoginType.qq.value
        if name.find('@') != -1:
            loginType = LoginType.email.value

        res = dbfunc.insertUploader(name, pwd, ext, platform, loginType)

        if res:
            print('添加'+self.platformItem['name']+'用户成功：' + name)
            button = QMessageBox.information(self, name, "添加成功", QMessageBox.Yes)
            if button:
                self.close()
                self.callback_sign.emit(platform)
                

# def main():
#     app = QApplication(sys.argv)
#     UserW = UserWidget()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()


