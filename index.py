import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import subprocess
import os



class Ffmpeg(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):

        self.infile = QLineEdit(self)
        self.outfile = QLineEdit(self)

        # ffplay = QLabel('去水印', self)

        xLabel = QLabel('X', self)
        yLabel = QLabel('Y', self)
        wLable = QLabel('W', self)
        hLabel = QLabel('H', self)

        self.xLabel = QLineEdit("1045")
        # self.xLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.yLabel = QLineEdit("45")
        # self.yLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.wLable = QLineEdit("195")
        # self.wLable.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.hLabel = QLineEdit("55")
        # self.hLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(self.infile, 0, 0)
        grid.addWidget(self.outfile, 1, 0)

        # grid.addWidget(ffplay, 0, 0)
        grid.addWidget(xLabel, 0, 1)
        grid.addWidget(self.xLabel, 0, 2)
        grid.addWidget(yLabel, 1, 1)
        grid.addWidget(self.yLabel, 1, 2)
        grid.addWidget(wLable, 2, 1)
        grid.addWidget(self.wLable,2, 2)
        grid.addWidget(hLabel, 3, 1)
        grid.addWidget(self.hLabel, 3, 2)
        
        ffplayButton=QPushButton("开始播放")
        ffplayButton.clicked.connect(self.playButtonClick)

        grid.addWidget(ffplayButton, 0, 3)

        ffmpegButton=QPushButton('开始去水印')

        ffmpegButton.clicked.connect(self.ffmpegButtonClick)

        grid.addWidget(ffmpegButton, 1, 3)

        # QToolTip.setFont(QFont('SansSerif', 10))
        self.resize(500, 150)
        self.move(100, 100)
        self.setWindowIcon(QIcon('./Title.ico'))
        self.setWindowTitle("去水印")

        self.setToolTip("<b>this is widget</b>")

        # btn = QPushButton("quit Button", self)  # self类似于C++ this指针
        # btn.setToolTip("This is a button will quit itself")
        # btn.clicked.connect(QCoreApplication.instance().quit)
        # btn.resize(btn.sizeHint())
        # btn.move(0, 0)
        self.show()

    def playButtonClick(self):
        
        # ffplay -i bb.mp4 -vf delogo=x=1045:y=45:w=195:h=55:show=1   
        infile = 'infile/'+self.infile.text()
        outfile = 'outfile/'+self.outfile.text()
        x = self.xLabel.text()
        y = self.yLabel.text()
        w = self.wLable.text()
        h = self.hLabel.text()


        strcmd = ['ffplay -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h+':show=1']
        result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
        print(result)

        
    def ffmpegButtonClick(self):


        
        # ffmpeg -i zy.mp4 -vf delogo=x=1048:y=45:w=195:h=55 3.mp4

        infile = 'infile/'+self.infile.text()
        outfile = 'outfile/'+ self.outfile.text()
        x = self.xLabel.text()
        y = self.yLabel.text()
        w = self.wLable.text()
        h = self.hLabel.text()

        path = 'infile'
        files = os.listdir(path)

        datas = []
        for file in files:
            if file.find('mp4') != -1:
                datas.append('infile/'+file)

        for data in datas:
            infile = data
            outfile = data.replace('infile/', 'outfile/')
            
            strcmd = ['ffmpeg -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h +' '+outfile]
            result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
            print(result)






if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Ffmpeg()

    sys.exit(app.exec_())
