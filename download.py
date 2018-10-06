import sys
import requests
import os
from config import *
import gfunc
import subprocess
import dbfunc

# 屏蔽warning信息
requests.packages.urllib3.disable_warnings()

'''
you-get
-o 设置路径
-O 设置下载文件的名称
--debug
'''
def cmd_download(url, filename, dirname=VIDEODIRNAME):

    gfunc.createDir(dirname)

    info = os.system(r'you-get -o {} -O {} {}'.format(dirname, filename, url))
    print(info)
    return filename

'''
ffmpeg 去水印 并删除原来的视频

'''
def cmd_watermark(filename, to_filename):
    infile = VIDEODIRNAME+'/'+filename
    outfile = VIDEODIRNAME+'/'+to_filename
    x, y, w, h = gfunc.get_watermark_size(filename)
    dd = 'ffmpeg -i ' +infile+' -vf delogo=x='+x+':y='+y+':w='+w+':h='+h +' '+outfile + ' -y'
    result = subprocess.check_call(dd, shell=True)
    if int(result) == 0:
        gfunc.removefile(infile)


'''
vid 腾讯视频url
'''
def get_vid(url):
    urlArr = url.split('/')
    vid = urlArr[len(urlArr)-1].replace('.html', '')
    return vid


def download_video(url):
    vid = get_vid(url)
    # 1 下载视频
    cmd_download(url, vid)
    # 2 去水印
    filename = vid+'.mp4'
    to_filename = vid+'_new'+'.mp4'
    cmd_watermark(filename, to_filename)
    return to_filename

def main(datas):
    for item in datas:
        is_exist_local = item[14]
        local_path = VIDEODIRNAME+'/'+item[15]
        url = item[3]
        idd = item[0]
        print(str(idd)+' :  '+local_path)

        if gfunc.isfile(local_path) == False or local_path.find('new') == -1:
            # 下载
            new_filename = download_video(url)
            # 存入数据库
            dic = {
                'is_exist_local': '1',
                'local_path': new_filename
            }
            dbfunc.updateVideo(dic, {'id': idd})

    # 重新获得数据库里的数据 是不是多此一举呢 todo
    dataArr = []
    for item in datas:
        res = dbfunc.getVideo({'id': item[0]})
        dataArr.append(res[0])

    return dataArr



# 获得真实地址 腾讯
def get_video_real_address(url):
    url = BASEURLTENCENTJX+url
    res = requests.get(url)
    text = res.text
    # 视频不存在
    if text.find('http') == -1:
        return ''
    url = re.findall("http:.*", text)[0]
    print(url)
    return url


def download(url, file_path):
    # 第一次请求是为了得到文件总大小
    r1 = requests.get(url, stream=True, verify=False)
    total_size = int(r1.headers['Content-Length'])

    # 这重要了，先看看本地文件下载了多少
    if os.path.exists(file_path):
        temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
    else:
        temp_size = 0
    # 显示一下下载了多少   
    print(temp_size)
    print(total_size)
    # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
    headers = {'Range': 'bytes=%d-' % temp_size}  
    # 重新请求网址，加入新的请求头的
    r = requests.get(url, stream=True, verify=False, headers=headers)

    # 下面写入文件也要注意，看到"ab"了吗？
    # "ab"表示追加形式写入文件
    with open(file_path, "ab") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                ###这是下载实现进度显示####
                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符


if __name__ == '__main__':
    # cmd_download('https://v.qq.com/x/page/e0733l5ikb9.html', 'filename')
    # cmd_video_size('filename.mp4')
    cmd_watermark('filename.mp4', 'dddd.mp4')
