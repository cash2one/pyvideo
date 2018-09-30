import jieba
import os
import sys
from config import *
import random
import json
import hashlib
import dbfunc
import requests
import re
import subprocess
import time



'''
分词
'''
def participle(str):
    # 自定义分词
    jieba.load_userdict('Source/userdict.txt')

    seg_list = jieba.cut(str)  # 默认是精确模式
    res_list = []
    # todo 删除一个词的
    for seg in seg_list:
        if len(seg) > 1:
                
            # TODO 特殊处理 徐老师来巡山
            if seg.find(u'徐老师来巡山') != -1:
                res_list.append('英雄联盟')
            res_list.append(seg) 
    
    return res_list

# [v2]
def classFromTitle(title):
    ups = Classly.keys()

    for item in ups:
        obj = Classly[item]
        tt = obj['type']
        data = obj['data']
        for ii in data:
            if title.find(ii) != -1:
                if tt == VideoType.comic:
                    return ['动漫', '动漫', item]
                if tt == VideoType.movie:
                    return ['电影', '电影剪辑', item]
                if tt == VideoType.game:
                    return ['游戏', '游戏', item]
                if tt == VideoType.tv:
                    return ['电视剧', '连续剧', item]
    # 【分类 分类 qq】
    return ['', '', '']

def createDir(dir):
    # if sys.version_info.major >= 3: # if the interpreter version is 3.X, use 'input',
    #     input_func = input          # otherwise use 'raw_input'
    # else:
    #     input_func = raw_input
    if os.path.exists(dir):
        pass
    else:
        os.makedirs(dir)  # Creates a new dir for the given name

def writeJsonFile(data, name, dirname='Source'):
    # 默认写入Source
    submit = './'+dirname+'/'+name+'.json'
    try:
        with open(submit, 'w') as f:
            json.dump(data, f)
            f.close()
    except Exception as e:
        pass

def readJsonFile(name, dirname='Source'):
    json_filename = './Source/'+name+'.json'
    try:
        with open(json_filename) as f:
            pop_data = json.load(f)
            f.close()
            return pop_data  
    except Exception as e:
        return None

# 文件是否存在
def isfile(file):
    return os.path.isfile(file)

# 文件夹是否存在
def exists(dir):
    return os.path.exists(dir)

def getLocalFile(dirname):
    try:
        for dirpath, dirnames, filenames in os.walk(dirname):
            print(filenames)

        return filenames
    except Exception as e:
        print(str(e))

    return []
    
def isLoginForLocal():
    data = readJsonFile('app')
    if data is None:
        return False
    else:
        try:
            return data['isLogin']
        except:
            return False

def setLoginForLocal(isLogin, name='', userId=''):
    data = readJsonFile('app')
    try:
        data['isLogin'] = isLogin
        data['name'] = name
        data['userId'] = str(userId)
    except:
        data = {
            'isLogin': isLogin,
            'name': name,
            'userId': str(userId)
        }
    writeJsonFile(data, 'app')

def getLoginNameForLocal():
    data = readJsonFile('app')
    return [data['isLogin'], data['name'], data['userId']]

def getUserId():
   data = readJsonFile('app')
   return data['userId']

def getUserName():
    data = readJsonFile('app')
    return data['name']

def isLogin():
    data = readJsonFile('app')
    return data['isLogin']

def pwdEncrypt(pwd):
    hl = hashlib.md5()
    hl.update(pwd.encode(encoding='utf-8'))
    md5pwd = hl.hexdigest()
    return md5pwd


def downVideo(url):
    base = 'http://www.ht9145.com/jx/tencent.php?url='
    url = base+url
    print(url)
    createDir('videos')        

    res = requests.get(url)
    text = res.text
    # 视频不存在
    # if text.find('http') == -1:
    #     return False
    url = re.findall("http:.*", text)[0]
    print(url)
    return writeFile(url)

def writeFile(url):
    urlArr = url.split('/')
    filename = ''
    for item in urlArr:
        if item.find('mp4') != -1:
            print(item)
            filename = item.split('?')[0]        

    filename = 'videos/'+filename
    print(filename)
    is_file = isfile(filename)
    if is_file == False:
        res = requests.get(url)
        
        # with closing(requests.get(url)) as response:
        data = res.content
        with open(filename, "wb") as code:
            if data:
                code.write(data)
            else:
                writeFile(url)
                return

        print('视频写入文件成功')
    else:
        print('视频已经下载')
    return filename

def watermarks(pagename):
    # new
    if pagename == None:
        return False
    if pagename.find('new') != -1:
        return False
    infile = pagename
    outfile =  pagename.replace('.mp4', '_new.mp4')

    x, y, w, h = getQuRectVideo(infile)
    strcmd = ['ffmpeg -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h +' '+outfile]
    result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
    print(result)
    return outfile

def getQuRectVideo(pagename):
    width, height = getVideoSize(pagename)
    return getQuSize(width, height)

# 视频的大小
def getVideoSize(pagename):
    bb = 'ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1 ' + pagename
    strcmd = [bb]
    result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
    stdout = result.stdout
    string = stdout.decode('utf-8')
    arr = string.split('\n')
    print(arr)
    width = arr[0].replace('width=', '')
    height = arr[1].replace('height=', '')
    return int(width), int(height)
# 去水印的大小
def getQuSize(width, height):
    x = ''
    y = ''
    w = ''
    h = ''

    # 960 x=690
    # 848-690=158
    print(width)
    if width < 1000:
        x = str(width-158)  
        y = '30'
        w = '135'
        h = '40' 
    return x, y, w,h

def downloadVideo(datas):
    print('检查本地是否有一个视频')
    for item in datas:
        is_exist_local = item[14]
        local_path = item[15]
        url = item[3]
        idd = item[0]
        print(str(idd)+' :  '+local_path)
        # TODO
        if isfile(local_path) == False:
            # 1. 下载 todo 视频不存在怎么处理
            local_path = downVideo(url)
            print(local_path)
            if (local_path):
            # 2. 存入数据库
                print('存入数据库')
                is_exist_local = '1'
                dic = {
                    'is_exist_local': is_exist_local,
                    'local_path': local_path
                }
                dbfunc.updateVideo(dic, {'id': idd})
            
        # 2.去水印
        if local_path:
            outfile = watermarks(local_path)

        print('存入去水印的视频')
        if outfile:
            dic = { 'local_path': outfile }
            dbfunc.updateVideo(dic, {'id': item[0]})

        time.sleep(1)
    print('下载完成去水印完成')

    dataArr = []
    for item in datas:
        res = dbfunc.getVideo({'id': item[0]})
        dataArr.append(res[0])

    return dataArr

def getVideosFromUploader(uploader):
    name = uploader[1]
    pwd = uploader[2]
    todayVideo = dbfunc.getTodayWartpublishVideo(name)
    allnum = 10
    makePubNum = allnum - len(todayVideo)

    if makePubNum > 0:
        return todayVideo[0:makePubNum]
    else:
        return []
    return []






        

        
         



