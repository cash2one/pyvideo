#encoding:utf-8
#name:mod_config.py

# python 2.7 import ConfigParser
# python 3.7 configparser

import configparser
import os

#获取config配置文件
''' 使用方法
dbname = mod_config.getConfig("database", "dbname")
'''
def getConfig(section, key):
    config = configparser.ConfigParser()
    # path = os.path.split(os.path.realpath(__file__))[0] + '/configure.conf'
    path = 'DBHelper/configure.conf'
    config.read(path, encoding='UTF-8')
    return config.get(section, key)

#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录