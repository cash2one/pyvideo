import requests
import json


def req_nmc():
	url = 'http://m.nmc.cn/f/rest/real/56294'
	headers = {
		'Referer': 'http://m.nmc.cn/publish/forecast/ASC/chengdu.html',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
	}
	r = requests.get(url, headers=headers)

	dd = r.json()
	print(dd)

req_nmc()