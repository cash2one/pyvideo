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
import contextlib
import progressbar

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
                    return ['动漫', '国产动漫', item]
                
                if tt == VideoType.game:
                    return ['游戏', '电脑电竞游戏（MOBA）', item]
                if tt == VideoType.tv:
                    return ['电视剧', '连续剧', item]
                if tt == VideoType.cinema:
                    return ['动漫', '少儿动漫', item]
                if tt == VideoType.movie:
                    return ['娱乐', '电影', item]
                if tt == VideoType.gc_comic:
                    return ['动漫', '国产动漫', item]
                if tt == VideoType.wz_game:
                    return ['游戏', '手机游戏', item]
                if tt == VideoType.cj_game:
                    return ['游戏', '手机游戏', item]

    # 【分类 分类 qq】
    return ['', '', '']

# [v3] 三级分类 todo second_class二级分类, qq 来判断
def getThirdClass(second_class, qq):
    if second_class == '少儿动漫':
        return '少儿动漫-其他'
    if second_class == '国产动漫':
        return '国产动漫-其他'
    if second_class == '日本动漫':
        return '日本动漫-其他'
    if second_class == '欧美动漫':
        return '欧美动漫-其他'
    if second_class == '电影':
        return '电影片段'
    # TODO
    if second_class == '手机游戏':
        if qq == '3056371919':
            return '王者荣耀玩家视频'
        if qq == '3216598385':
            return '吃鸡'
    
    if second_class == '电脑电竞游戏（MOBA）':
        return '英雄联盟玩家视频'

    return ''


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
# 文件删除
def removefile(file):
    if isfile(file):
        os.remove(file)


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

'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


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

# 根据url 获得MP4文件名
def get_FileNameFromUrl(url):
    urlArr = url.split('/')
    filename = ''
    for item in urlArr:
        if item.find('mp4') != -1:
            filename = item.split('?')[0]        

    filename = 'videos/'+filename
    return filename

def writeFile(url):
    filename = get_FileNameFromUrl(url)
    print(filename)
    is_file = isfile(filename)
    if is_file == False:
        
        return writeLocal(url, filename)
        
    else:
        print('视频已经下载')
        # 计算大小 MB
        filesize = get_FileSize(filename)
        if filesize < 0.1:
            # TODO 是否要先删除文件
            removefile(filename)
            # 重新下载
            return writeLocal(url, filename)



    return filename

def writeLocal(url, filename):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Proxy-Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

        }
        resp = requests.get(url, stream=True, headers=headers)
        # print(resp.content)
        total_length = int(resp.headers.get("Content-Length"))
        print('video total length: '+ str(total_length))

        with open(filename, "wb") as f:
            widgets = ['Progress: ', progressbar.Percentage(), ' ',
                   progressbar.Bar(marker='#', left='[', right=']'),
                   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()

            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

                pbar.update(len(chunk) + 1)
            pbar.finish()
            print('视频写入成功')
            return filename
    except Exception as e:
        print('视频写入失败：'+str(e))
        # todo 写入错误 删除文件
        removefile(filename)
        writeLocal(url, filename)

def watermarks(pagename):
    # new
    if pagename == None:
        return False
    if pagename.find('new') != -1:
        return False
    infile = pagename
    outfile =  pagename.replace('.mp4', '_new.mp4')

    x, y, w, h = getQuRectVideo(infile)
    strcmd = ['ffmpeg -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h +' '+outfile + ' -y']
    result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
    print(result)
    return outfile

def getQuRectVideo(pagename):
    width, height = getVideoSize(pagename)
    return getQuSize(width, height)

# 视频的高宽
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

'''
[v3]
ffmpeg
ffprobe
获得本地视频的宽度 高度
'''
def get_video_size(filename):
    filepath = VIDEODIRNAME+'/'+filename
    show = 'ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1 ' + filepath
    string = subprocess.check_output(show, shell=True)
    string = string.decode('utf-8')
    print(string)
    arr = string.split('\n')
    width = arr[0].replace('width=', '')
    height = arr[1].replace('height=', '')
    return int(width), int(height)

'''
[v3]
width   1280 x=1045:y=45:w=195:h=55
        960  x=width-158:y=30:w=135:h=40
        450  x=width-100:y=15:w=90:h=30

获取水印的大小 根据本地视频
x y w h
'''
def get_watermark_size(filename):
    width, height = get_video_size(filename)
    if width > 1000:
        return str(width-235), '45', '195', '55'
    elif 500 < width < 1000:
        return str(width-158), '30', '135', '40'
    else:
        return str(width-100), '15', '90', '30'

'''
获得视频第五秒的图片
'''
def get_image_video(pathname):
    outfile = pathname.replace('.mp4', '.jpg')
    show = 'ffmpeg -ss 00:00:16 -i %s -frames:v 1 %s -y' % (pathname, outfile)
    string = subprocess.check_output(show, shell=True)
    return outfile




# 去水印的大小
def getQuSize(width, height):
    x = ''
    y = ''
    w = ''
    h = ''

    # 960 x=690
    # 848-690=158
    print(width)
    if 500 < width < 1000:
        x = str(width-158)  
        y = '30'
        w = '135'
        h = '40' 

    if width < 500:
        x = str(width-100)  
        y = '15'
        w = '90'
        h = '30'

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

        print('存入去水印的视频：')
        if outfile:
            # 验证是否有大于100kb
            if get_FileSize(outfile) > 0.1:
                # 移除源文件
                removefile(local_path)

                dic = { 'local_path': outfile }
                dbfunc.updateVideo(dic, {'id': item[0]})
            else:
                print('视频怎么这么小呢，删除了')
                removefile(outfile)
                # 重新下载 或者重新去水印

        time.sleep(1)
    print('下载完成去水印完成')

    dataArr = []
    for item in datas:
        res = dbfunc.getVideo({'id': item[0]})
        dataArr.append(res[0])

    return dataArr

def getVideosFromUploader(uploader, datas=[]):
    name = uploader[1]
    pwd = uploader[2]
    todayPubVideo = dbfunc.getTodayPublishedVideo(name)
    allnum = 10
    makePubNum = allnum - len(todayPubVideo)
    if makePubNum > 0:
        if len(datas) > 0:
            todayVideo = datas
        else:
            todayVideo = dbfunc.getTodayWartpublishVideo(name)
        if makePubNum >= len(todayVideo):
            return todayVideo
        else:
            return todayVideo[0:makePubNum]
    else:
        return []
    return []

