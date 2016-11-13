# -*- coding: utf-8 -*-
"""
Todo: sync https://raw.githubusercontent.com/racaljk/hosts/master/hosts to
/etc/hosts
"""

import os
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

    if os.path.exists(output_file):
        opfile = open(output_file, 'ab')
        exist_size = os.path.getsize(output_file)
        Urlclass.addheader('Range', 'bytes={}-'.format(exist_size))
    else:
        opfile = open(output_file, 'wb')
        exist_size = 0

    page = Urlclass.open(url)
    #if verbose:
    #    for k, v in page.headers.items():
    #        print('{}={}'.format(k, v))
    num_bytes = 0
    web_size = int(page.headers['Content-Length'])
    if web_size == exist_size:
        if verbose:
            print('File ({}) was already downloaded from URL ({})'.format(output_file, url))
    else:
        if verbose:
            print('Downloading {} more bytes'.format(web_size - exist_size))
        while True:
            data = page.read(8192)
            if not data:
                break
            opfile.write(data)
            num_bytes = num_bytes + len(data)
    page.close()
    opfile.close()
    if verbose:
        print('downloaded {} bytes from {}'.format(num_bytes, page.url))

    return num_bytes


def main():
    #url = 'https://raw.githubusercontent.com/racaljk/hosts/master/hosts'
    url = 'http://mirrors.163.com/gentoo/releases/amd64/autobuilds/20161108/systemd/stage3-amd64-systemd-20161108.tar.bz2'
    print(download_file(url, 'hosts.dl', 1))


if __name__ == '__main__':
    main()
