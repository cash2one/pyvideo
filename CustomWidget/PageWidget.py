from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class PageWidget(QWidget):
    def __init__(self,parent=None):
        super(PageWidget,self).__init__(parent)
        self.btns=[]
        self.count=0

        self.allnum = 5

        self.presign=0           #当前点击标识
        self.nextsign=0         #当前点击标识
        self.pre_button=QPushButton()
        self.pre_button.setText("上一页")
        # self.pre_button.setFixedSize(25,25)
        self.pre_button.clicked.connect(self.prepage)
        self.next_button=QPushButton()
        self.next_button.setText("下一页")
        self.next_button.clicked.connect(self.nextpage)
        # self.next_button.setFixedSize(25,25)
        self.center_layout=QHBoxLayout()
        self.center_page()

        self.page_layput=QHBoxLayout()
        self.page_layput.addWidget(self.pre_button)
        self.page_layput.addLayout(self.center_layout)
        self.page_layput.addWidget(self.next_button)
        self.setLayout(self.page_layput)

    def center_page(self):
        for index in range(1, self.allnum):
            button = QPushButton()
            button.setText(str(index))
            button.clicked.connect(self.clickpage)
            self.center_layout.addWidget(button)


    def clickpage(self):
        print('111')
            

 
    def prepage(self):
        self.presign=1
        self.num=0
        if (len(self.btns)>0) and (self.count>=10):
            for p in range(10):
                self.center_layout.removeWidget(self.btns[p])
                self.btns[p].deleteLater()
            self.btns=[]
        if self.count>=10:
            if self.nextsign==1:
                self.count=self.count-20
                self.nextsign=0
            else:
                self.count=self.count-10
            self.num=self.count
 
            for i in range(10):
                self.num+=1
                self.center_button=QPushButton()
                self.center_button.setText(str(self.num))
                # self.center_button.setFixedSize(25,25)
                self.btns.append(self.center_button)
                self.center_layout.addWidget(self.center_button)

    def nextpage(self):
        self.nextsign=1
        if len(self.btns)>0:
            for p in range(10):
                self.center_layout.removeWidget(self.btns[p])
                self.btns[p].deleteLater()
            self.btns=[]
        if self.presign==1:
            self.count=self.count+10
            self.presign=0
        #mapper转有参数
        signal_mapper = QSignalMapper(self)
        for i in range(10):
            self.count+=1
            self.center_button=QPushButton()
            self.center_button.setText(str(self.count))
            # self.center_button.setFixedSize(25,25)
            self.btns.append(self.center_button)
            self.center_button.clicked.connect(self.prepage)
            signal_mapper.setMapping(self.center_button, str(self.count))
            self.center_layout.addWidget(self.center_button)
        signal_mapper.mapped.connect(self.showpage)
 
    def showpage(self,page):
        print('111')
 
if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    page=PageWidget()
    page.show()
    sys.exit(app.exec_())