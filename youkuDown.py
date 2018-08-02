import re
import urllib.request
import json
import time
import random
import sys

def getVideoInfo(url):
	ruleTitle=re.compile('<title>(.*)</title>')
	ruleId=re.compile('v.youku.com/v_show/id_(.*).html')
	videoTitle=ruleTitle.findall(urllib.request.urlopen(url).read().decode('utf8'))
	videoId=ruleId.findall(url)
	print(videoId)
	return videoTitle[0],videoId[0]
    

def getTrueLink(videoid):
    url = 'https://ups.youku.com/ups/get.json?vid='+videoid+'&ccode=0401&client_ip=192.168.1.1&utid=iPMOEU7K4zsCAbTVE5gQjsU7&client_ts=1496141317&playlist_id=49981133&ob=1'

	data = urllib.request.urlopen(url)

	info=json.loads(data.read().decode('utf8'))
	print(info)
	

def down2file(urls,filename):
	f=open(filename,'wb')
	fileNum=len(urls)
	count=0
	for url in urls:
		count+=1
		print('downloading file %d/%d'%(count,fileNum))
		req=urllib.request.Request(url,headers={'Referer':'http://www.youku.com'})
		data=urllib.request.urlopen(req).read()
		f.write(data)
	f.close()
	print('download '+filename+' OK!')

def youkuDown(link):
    
	print(link)
	videotitle,videoid=getVideoInfo(link)
	getTrueLink(videoid)
	# down2file(urls,videotitle+'.flv')

if __name__=='__main__':
	if len(sys.argv)<2:
		print('Example Usage: python3 youkuDown.py https://v.youku.com/v_show/id_XMzYzMjk0MDA2OA==.html')
		print('')
		exit() 
	youkuDown(sys.argv[1])
