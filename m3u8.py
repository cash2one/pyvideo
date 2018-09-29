#coding: utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import gevent
import requests
import urlparse
import os
import time

class Downloader:
    def __init__(self, pool_size, retry=3):
        self.pool = Pool(pool_size)
        self.session = self._get_http_session(pool_size, pool_size, retry)
        self.retry = retry
        self.dir = ''
        self.succed = {}
        self.failed = []
        self.ts_total = 0

    def _get_http_session(self, pool_connections, pool_maxsize, max_retries):
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=max_retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session

    def run(self, m3u8_url, dir=''):
        self.dir = dir
        if self.dir and not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        r = self.session.get(m3u8_url, timeout=10)
        if r.ok:
            body = r.content
            if body:
                ts_list = [urlparse.urljoin(m3u8_url, n.strip()) for n in body.split('\n') if n and not n.startswith("#")]
                ts_list = zip(ts_list, [n for n in xrange(len(ts_list))])
                if ts_list:
                    self.ts_total = len(ts_list)
                    print(self.ts_total)
                    g1 = gevent.spawn(self._join_file)
                    self._download(ts_list)
                    g1.join()
        else:
            print(r.status_code)

    def _download(self, ts_list):
        self.pool.map(self._worker, ts_list)
        if self.failed:
            ts_list = self.failed
            self.failed = []
            self._download(ts_list)

    def _worker(self, ts_tuple):
        url = ts_tuple[0]
        index = ts_tuple[1]
        retry = self.retry
        while retry:
            try:
                r = self.session.get(url, timeout=20)
                if r.ok:
                    file_name = url.split('/')[-1].split('?')[0]
                    print(file_name)
                    with open(os.path.join(self.dir, file_name), 'wb') as f:
                        f.write(r.content)
                    self.succed[index] = file_name
                    return
            except:
                retry -= 1
        print('[FAIL]%s' % url)
        self.failed.append((url, index))

    def _join_file(self):
        index = 0
        outfile = ''
        while index < self.ts_total:
            file_name = self.succed.get(index, '')
            if file_name:
                infile = open(os.path.join(self.dir, file_name), 'rb')
                if not outfile:
                    outfile = open(os.path.join(self.dir, file_name.split('.')[0]+'_all.'+file_name.split('.')[-1]), 'wb')
                outfile.write(infile.read())
                infile.close()
                os.remove(os.path.join(self.dir, file_name))
                index += 1
            else:
                time.sleep(1)
        if outfile:
            outfile.close()

if __name__ == '__main__':
    downloader = Downloader(50)
    # url = 'http://pl-ali.youku.com/playlist/m3u8?vid=XMzYzMjk0MDA2OA%3D%3D&type=hd2&ups_client_netip=dded2e63&utid=iTbUE8VuE3ECAXZyBV8VD0xE&ccode=0512&psid=38fbd7be3bd83e3abe1f537a09cf991c&duration=295&expire=18000&drm_type=1&drm_device=7&ups_ts=1533090628&onOff=0&encr=0&ups_key=0bb2f500fbafbccb45fc45258c4f3e2e'
    # url = 'http://183.66.104.115/sportsts.tc.qq.com/AVIo9SUuntMHJ8anwe6vTUC2lRA09JDybd6yx6IjCNX8/4TDxaVQl2c132vUv5tFfXzGfYLtKfOwKC2EzGvSurKakB18tMGyiuKgi_qrMuZsvoZKCEZTqb_HWymMxAymXXkwVWc-PiWcjjZeWVJcKLrJ0pBs_rkTS0Q/t0027ynq4y3.321003.ts.m3u8?ver=4'
    # url = 'http://ltsbsy.qq.com/uwMRJfz-r5jAYaQXGdGnCtD0ZkRh8BgOUQePMGh65cs/ZL5mczBKBiRr0gPwt4Kp1ZEqTKJEMlN37uO5ASCpifEj-c9wT_oPOavgD0DYxI9WvbaNRw09DrWkyxMdJzv-f5E9ycyUak_yqqUeGgyXWcirKWXxEN4Pzw/g0027mj8rbi.321003.ts.m3u8?ver=4'
    # url = 'http://61.128.151.150/sportsts.tc.qq.com/ANrdIeTsydtFT2TDk9KX5-lgTMatCwpOntG9JbJXD-HQ/H8NtiKJxSHbzsnJ12EamCeofeXBJZb-4TIOUhA2iJw-IuGsN-LJFqUL_TsvhCFBqCb8Mhc9xIJ5xLn9or9-GwJ1qT9Juj3TzHDznwa8-m4Rji18y1mMJFQ/i00275sy7c8.321003.ts.m3u8?ver=4'
    # url = 'https://apd-36a3064ef9c9799ef676f73b64a88e94.v.smtcdns.com/moviets.tc.qq.com/A4wuQTx1lgG3nM7RjZ7MNhqWQiwUixAoAs0RYd5lvU0Y/uwMRJfz-r5hgYaQXGdGnCwQsKf_dEsnq3UJztMoyPd8/YeyHZHPz-gAEhvB5eGGFBqz71voe2PUGLbt8lFwR6WcQIL0jiKK1R8FpiFeSoQgqBYTKkh5EtdI-snLK8S6wt0caNIL0bPCG9VliO0xW9Rz556u-rRnOLfgnobexXVa5jRZQDBe92i55593Qn3FOjGcuL-P5AcCg/g0025k58ole.321003.ts.m3u8?ver=4'
    # url = 'https://apd-60c1fec4f8cd07f7dd7f0dda8f0e3418.v.smtcdns.com/moviets.tc.qq.com/A3vI0dQ_Chs1Sx2qTykUSw6sVIGkFMCs94m75sR07cD8/uwMRJfz-r5hgYaQXGdGnCwQsKf_dEsnq3UJztMoyPd8/WN4cFfYNNFczStMlc2dh_o4bwMoQJEFRHdRZZAXKgTi_l1Tx6nmwUGg_DmnxpgWEpZaOB2PCGY68o1G4Efztx7YQNDetZCMDyoBAMrEsybqV8bnpWn3_nko8RsONsRA1t7h3SmlLb5_Xriq3v2pqRgr6Iw97bUj-/l00258785m2.321004.ts.m3u8?ver=4'
    # url = 'https://apd-a150458ce3b41024f60706cac3182545.v.smtcdns.com/moviets.tc.qq.com/AKE9pH95OyNM2xYWaTFvDSqzAzKv6NipJK_1S9rWDWa4/uwMRJfz-r5hgYaQXGdGnCwQsKf_dEsnq3UJztMoyPd8/KRiof2o-OsknaQ_APwUSakdWVoKcXAk6RaAg9PzpmjbPS8vYiUDUKG2BYeSZ4Gvjht8IdNPHbF3kF2hgafn3nJR0-m44zjIDDyl9f93NvBAkSjsHKICDKBScIXJED31MWQl8a6r1ZE4yXgCoy4EfUBFW2kaQyLtO/d00256t4te2.321004.ts.m3u8?ver=4'
    url = 'https://apd-ff0c565e65257acf9ffaf26967cc833b.v.smtcdns.com/moviets.tc.qq.com/An0FKGYV2EyyuJvw-DpyKCKOfw868iCmrZkg9ZRavHJk/uwMRJfz-r5hgYaQXGdGnCwQsKf_dEsnq3UJztMoyPd8/f1sn5EhNhqmoOPihxkjBlA2rSwJ2wpsvhQRqfkiDUFq_AhYgzB3iakIJA5aA_vr-JKvpMMduyrKX_YcP2QrXQtkNKtynwwPJOgdPFq65dEInAmRa8pNxU82bwmqSVsiepQ7phD5yOK984gZ0a-n4hTuOswWMTxQs/o0025ibcdpo.321004.ts.m3u8?ver=4'
    downloader.run(url, '')
