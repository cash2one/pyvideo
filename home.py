import sys
from PyQt5.QtWidgets import QApplication
import Login

app = QApplication(sys.argv)
login = Login.Login()

sys.exit(app.exec())