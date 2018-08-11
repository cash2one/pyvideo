import requests
import json

# https://v.qq.com/x/page/a07518vbjln.html
def getvid_tx(txurl):
    vid = txurl.replace('.html', '').split('/')[-1]
    print(vid)
    return vid

def jiexi_tx(txurl):
    vid = getvid_tx(txurl)
    urlarr = []
    for definition in ('sd', 'hd', 'shd'):
        params = {
            'isHLS': False,
            'charge': 0,
            'vid': vid,
            'defn': definition,
            'defnpayver': 1,
            'otype': 'json',
            'platform': 10901,
            'sdtfrom': 'v1010',
            'host': 'v.qq.com',
            'fhdswitch': 0,
            'show1080p': 1,
        }
        r = requests.get('http://h5vv.video.qq.com/getinfo', params=params)
        data = json.loads(r.content[len('QZOutputJson='):-1])
        url_prefix = data['vl']['vi'][0]['ul']['ui'][0]['url']
        for stream in data['fl']['fi']:
            if stream['name'] != definition:
                continue
            stream_id = stream['id']
            urls = []
            try:
                ci = data['vl']['vi'][0]['cl']['ci']
            except Exception as e:
                ci = None

            if ci is None:
                break

            for d in ci:
                keyid = d['keyid']
                filename = keyid.replace('.10', '.p', 1) + '.mp4'
                params = {
                    'otype': 'json',
                    'vid': vid,
                    'format': stream_id,
                    'filename': filename,
                    'platform': 10901,
                    'vt': 217,
                    'charge': 0,
                }
                r = requests.get('http://h5vv.video.qq.com/getkey', params=params)
                data = json.loads(r.content[len('QZOutputJson='):-1])
                url = '%s%s?sdtfrom=v1010&vkey=%s' % (url_prefix, filename, data['key'])
                urls.append(url)

            # print('stream:', stream['name'])
            # print(str(urls))
            if len(urls) > 0:
                dic = {'stream': stream['name'], 'urls': urls}
                urlarr.append(dic)
    print(urlarr)
    return urlarr

# jiexi_tx('https://v.qq.com/x/page/d0741am37rh.html')

