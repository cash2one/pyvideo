from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import dbfunc

class UserWidget(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
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
        self.setWindowTitle('添加看点用户')
        # self.show()

    def btnClick(self):
        name = self.name.text()
        pwd = self.pwd.text()
        ext = self.ext.text()

        if len(name) == 0 or len(pwd) == 0:
            QMessageBox.warning(self, '', "请输入账号和密码", QMessageBox.Yes)
            return
        
        res = dbfunc.insetkdUser(name, pwd, ext)

        if res:
            print('添加看点用户成功：' + name)
            button = QMessageBox.information(self, name, "添加成功", QMessageBox.Yes)
            if button:
                self.close()
                self.callback(name)

# def main():
#     app = QApplication(sys.argv)
#     UserW = UserWidget()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()


