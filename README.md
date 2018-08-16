# pyvideo
py

进入终端，切路径至该文件夹下
cd ~/Desktop/transapp
1
开始产生初始化文件
py2applet --make-setup translate.py
1
保险起见，清除以前产生的build和dist文件夹，第一次操作这两个文件夹是没有的
rm -rf build dist
1
开始打包应用
python setup.py py2app
