import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Login(QDialog):
    """登录窗口"""
    def __init__(self, *args):
        super(Login, self).__init__(*args)
        loadUi('Login.ui', self)   #看到没，瞪大眼睛看

