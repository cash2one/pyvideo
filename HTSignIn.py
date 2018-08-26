import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import hashlib
from PyQt5.QtSql import *
import dbfunc


class SignInWidget(QWidget):
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super(SignInWidget, self).__init__()
        self.setUpUI()

    def setUpUI(self):
        self.Vlayout = QVBoxLayout(self)
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.formlayout = QFormLayout()

        self.label1 = QLabel("账号: ")
        labelFont = QFont()
        labelFont.setPixelSize(18)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.label1.setFont(labelFont)
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedHeight(32)
        self.lineEdit1.setFixedWidth(180)
        self.lineEdit1.setFont(lineEditFont)
        self.lineEdit1.setMaxLength(10)

        self.formlayout.addRow(self.label1, self.lineEdit1)

        self.label2 = QLabel("密码: ")
        self.label2.setFont(labelFont)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedHeight(32)
        self.lineEdit2.setFixedWidth(180)
        self.lineEdit2.setMaxLength(16)

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit1.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEdit2.setValidator(pValidator)

        passwordFont = QFont()
        passwordFont.setPixelSize(10)
        self.lineEdit2.setFont(passwordFont)

        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.formlayout.addRow(self.label2, self.lineEdit2)
        self.signIn = QPushButton("登 录")
        self.signIn.setFixedWidth(80)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)
        self.formlayout.addRow("", self.signIn)

        self.label = QLabel("欢迎使用看点自动测试系统")
        fontlabel = QFont()
        fontlabel.setPixelSize(30)
        self.label.setFixedWidth(400)
        # self.label.setFixedHeight(80)
        self.label.setFont(fontlabel)
        self.Hlayout1.addWidget(self.label, Qt.AlignCenter)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)
        self.widget2 = QWidget()
        self.widget2.setFixedWidth(300)
        self.widget2.setFixedHeight(150)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)
        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)
        self.Vlayout.addWidget(self.widget1)
        self.Vlayout.addWidget(self.widget, Qt.AlignTop)

        self.signIn.clicked.connect(self.signInCheck)
        self.lineEdit2.returnPressed.connect(self.signInCheck)
        self.lineEdit1.returnPressed.connect(self.signInCheck)

    def signInCheck(self):
        name = self.lineEdit1.text()
        password = self.lineEdit2.text()
        if (name == "" or password == ""):
            print(QMessageBox.warning(self, "警告", "用户和密码不可为空!", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库连接
        res = dbfunc.fetchUserFromName(name)
        # md5编码
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        md5password = hl.hexdigest()

        if res == False or len(res) == 0:
            # TODO 不存在 创建用户
            dbfunc.insetUser(name, md5password)
            self.login(name, md5password, None)
        else:
            self.login(name, md5password, res)

    def login(self, name, password, res=None):
        if res is not None:
            # TODO 验证 密码
            if password == res[0][2] and res[0][1] == name:
                self.login_signal.emit(name, str(res[0][0]))
            else:
                # 密码错误
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            # 登录
            # 
            print
            res = dbfunc.fetchUserFromName(name)
            print(res)
            self.login_signal.emit(name, str(res[0][0]))


