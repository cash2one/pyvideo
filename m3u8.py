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
    urls = [
        # 'https://apd-4f7fc087ddc9fae42753cf007ffbdc9e.v.smtcdns.com/sportsts.tc.qq.com/AisR9J2j9Tuan2QmRVoDvRbg4Gu07YnuYZ3h-dpTrU6Q/6WDFKE_3MS4oJvDYL6lr9PKGgjbuaD39IlqOhODWEFjeZ-dYNUg2EBdnSAye7lYlXJyebYEtXfDucbeYivg0Gb33cvKC3r5IisNR1A_5wfnKwhwu5Cs22xvdKsSuex1HhnEeqxAdsE7Y_y112W2-aKJLcht5x1KS/v0027g56cwe.321003.ts.m3u8?ver=4',
        # 'https://apd-da72055aec33e26527c552c05ea6ba10.v.smtcdns.com/sportsts.tc.qq.com/A3gtvlDBItXBqVB3ROO3yXOflhE_rfQmvJ6SYlg7Ld_E/ZJTbiVG2l2VyEC2SxzHOLvUrNajNasGh0_33RlBNrQ8mfIgNLk3pi_JcbsBaCHl7zOtfPurxzoTtoNyJd_SXISbIcVpwmKdLYi4VkonogSckch5O_0JJGpyv0EHvOxD48ZElxFwKHwEmzECaPuL9NWWW3GNozjEm/y0027wib6gl.321003.ts.m3u8?ver=4',
        # 'https://apd-7676325332803fa71d2ea55232e16b4c.v.smtcdns.com/sportsts.tc.qq.com/A-Jot-T84we2MT0CTL-kQlk9MEw0Y13wfrsP1_dk9zqQ/A39-xrWRmR6801KS1cncZjX7u3evrGJzS6ZYeCbWjkCp6DHOXETKd27UK_Xof1ljT2h9mkjHgYLDNBVtzapGYqDestiEpOSfv8aPvAXy22qm3VNdBLJnm8Pvq2i8H4d-MDh6-_6doXqYTfzUUPD1vCxCpN_MI_q4/g0027jr26hp.321003.ts.m3u8',
        # 'https://apd-f4ab557363ab26ce964e0c7ed77c6b96.v.smtcdns.com/sportsts.tc.qq.com/A3TTnuaDVBeZnUKA9pFkFj3KYNa_5VF2-GmE4DV-O3fQ/OxxKtRbrtFA5INFNzpKlSJKab4oHlLDy8yseL9Do1M73z9KbVTlNaMC0HKEBd7Xp-YYe5pYWIVYvuqz4Cu_o8AcEGckNj2dASBYjXPXBE3_pAC-ym50ksAo2Y4npAcwmT3CW4w2tAK3i-JhcI0r2OS8JFwbvzXSv/w0027jhwjvv.321003.ts.m3u8?ver=4',
        # 'https://apd-2383372cc465d3b73d760fbb1ea2e0ff.v.smtcdns.com/moviets.tc.qq.com/A1HUYGu8UnskQhtcHLuNDIdiSrHokgUG_4vWnOFBI0HE/GcmrT2cO4hqfdcq22g4vpmQUvC-oOSeOO-15NFtU7NK90auioy2XHZEGpRBQTssgRuuXrEV1NiXl-UEjjkolRVKd2sOd72sb-AHj74BKfeA95jXGwXnUOZt7-QB8cxFRcbW9N1V-vUvCARIH-R242BwlruRaEOYG/d0027j9renh.321003.ts.m3u8?ver=4',
        'https://apd-b0e2e60de0e3b19b61ef9876dd7f08d6.v.smtcdns.com/vipts.tc.qq.com/A5vVkIWnu95KBqAhaDF3eT8lU2qy42BlcFj3DKBPgDUo/NQUhmKjPtG6edB0UVIHjl8h1dstxx8zUPtVxBuNFFCe9NHJ7yACPcl9weR6NULjnq0wnw-Xz4Sr-xqMSEIOWb5oVIkL33LpkRk3sK__iUKmOfGri5DOklQONbqxMgl9GBY6bvsTIrQzQBZiuIKqx2AjNqAMrvMbm/070_e0027x9f4bn.321003.ts.m3u8?ver=4'
    ]

    # 【团战】丝毫不给活路越塔就是杀 RSG带兵线强势扳回一城
    # 【团战】RSG控制链无解 扁鹊爆毒连收两人
    for url in urls:
        downloader.run(url, '')
