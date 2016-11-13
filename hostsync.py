# -*- coding: utf-8 -*-
"""
Todo: sync https://raw.githubusercontent.com/racaljk/hosts/master/hosts to
/etc/hosts
use Etag and Content-Range
"""

import os
import shutil
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
try:
    from urllib.request import FancyURLopener
except ImportError:
    from urllib import FancyURLopener


class URLOpener(FancyURLopener):

    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass


def download_file(url, output_file, verbose=0):
    """
    :type url: str 要下载的url
    :type output_file: str of path 下载的文件
    :type verbose: int
    :rtype: int
    """
    Urlclass = URLOpener()

    page = Urlclass.open(url)
    if verbose:
        for k, v in page.headers.items():
            print('{}={}'.format(k, v))

    # Etag
    new_source = False
    etag = page.headers.get('Etag')
    if etag:
        etag_file = output_file + '.etag'
        if os.path.exists(etag_file):
            if etag != open(etag_file).read():
                new_source = True
        else:
            f = open(etag_file, 'w')
            f.write(etag)
            f.close()

    if os.path.exists(output_file) and not new_source:
        opfile = open(output_file, 'ab')
        exist_size = os.path.getsize(output_file)
        Urlclass.addheader('Range', 'bytes={}-'.format(exist_size))
    else:
        opfile = open(output_file, 'wb')
        exist_size = 0

    num_bytes = 0
    web_size = int(page.headers['Content-Length'])
    web_range = page.headers.get('Content-Range')
    if web_size == exist_size:
        if verbose:
            print('File ({}) was already downloaded from URL ({})'.format(output_file, url))
        if etag:
            if os.path.exists(etag_file):
                os.remove(etag_file)
    else:
        if verbose:
            print('Downloading {} more bytes'.format(web_size - exist_size))
        while True:
            data = page.read(8192)
            if not data:
                break
            opfile.write(data)
            num_bytes = num_bytes + len(data)
        if etag:
            if os.path.exists(etag_file):
                os.remove(etag_file)
    page.close()
    opfile.close()
    if verbose:
        print('downloaded {} bytes from {}'.format(num_bytes, page.url))

    return num_bytes


def main():
    url = 'https://raw.githubusercontent.com/racaljk/hosts/master/hosts'
    src_file = '/tmp/hosts.dl'
    dst_file = '/etc/hosts'
    download_file(url, src_file, 1)
    shutil.copyfile(src_file, dst_file)
    


if __name__ == '__main__':
    main()
