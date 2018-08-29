import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from SignIn import SignInWidget
import sip
from home import Home
from config import *
import gfunc

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")
        self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.quitAction = QAction("退出", self)

        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        self.Menu.triggered[QAction].connect(self.menuTriggered)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)

        isLogin = gfunc.isLoginForLocal()
        if isLogin:
            self.widget = Home()
            self.setCentralWidget(self.widget)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(True)
        else:
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.login_signal[str, str].connect(self.loginSuccess)


    def loginSuccess(self, name, userId):
        sip.delete(self.widget)
        gfunc.setLoginForLocal(True, name, userId)

        self.widget = Home()
        self.setCentralWidget(self.widget)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)
        

    def menuTriggered(self, q):
        if (q.text() == "退出登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.login_signal[str, str].connect(self.loginSuccess)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
            gfunc.setLoginForLocal(False)

        if (q.text() == "登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.login_signal[str, str].connect(self.loginSuccess)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出"):
            qApp = QApplication.instance()
            qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./Source/app.png'))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    rect = QApplication.desktop().screenGeometry()
    mainMindow.resize(rect.width(), rect.height())
    mainMindow.setWindowTitle('看点自动测试')
    # mainMindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    mainMindow.show()
    sys.exit(app.exec_())
