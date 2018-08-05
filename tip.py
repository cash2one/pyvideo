from PyQt5.QtWidgets import *


def show(parent, title='', detail=''):
    QMessageBox.warning(parent,
                            title,  
                            detail,  
                            QMessageBox.Yes | QMessageBox.No)