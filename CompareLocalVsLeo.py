import os
import sys
import json
import requests
import urllib.request

import bs4
from bs4 import BeautifulSoup

# Please add your own path, and ensure the 'DIR' names match your folder inner folder structure!!
DIRECTORY = 'C:\\Users\\Tom\\Music\\Cover songs\\'

# URLS to Dropbox removed. Please add your own!!
DROPBOX_DIR_URL = [
    {
        'DIR': 'Acoustic Covers',
        'URL': ''
    },
    {
        'DIR': 'Christmas Metal Covers',
        'URL': ''
    },
    {
        'DIR': 'Metal Medleys',
        'URL': ''
    },
    {
        'DIR': 'Misc',
        'URL': ''
    },
    {
        'DIR': 'Volume 1-5',
        'URL': ''
    },
    {
        'DIR': 'Volume 6-15',
        'URL': ''
    }
]


def get_web_document(url):
    return requests.get(url).text


def download_missing_song(dropbox_song, dir):
    download_song_url = dropbox_song['file_url'].replace('?dl=0', '?dl=1')
    download_song_dir = DIRECTORY+dir+'\\'+dropbox_song['file_name']
    urllib.request.urlretrieve(download_song_url, download_song_dir, download_report_hook)
    print('DOWNLOAD SUCCESSFUL @ ' + download_song_dir+'\n')


def download_report_hook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        sys.stderr.write('\r%5.1f%% %*d / %d' % (percent, len(str(totalsize)), readsofar, totalsize))
        if readsofar >= totalsize:
            sys.stderr.write('\n')
    else:
        sys.stderr.write('read %d\n' % readsofar)


def compare_local_vs_dropbox(dropbox_files, dir):
    none_missing = False
    local_song_list = os.listdir(DIRECTORY+dir)
    dropbox_song_list = []

    for file in dropbox_files:
        dropbox_song_list.append({
            'file_name': file['filename'],
            'file_url': file['href']
        })

    for dropbox_song in dropbox_song_list:
        if dropbox_song['file_name'] not in local_song_list:
            print('MISSING: ' + dropbox_song['file_name'])
            print('DOWNLOADING: ' + dropbox_song['file_name'])
            download_missing_song(dropbox_song, dir)
            none_missing = False
        else:
            none_missing = True

    if none_missing:
        print(dir + ' UP TO DATE\n------------------------------------------')


def parse_dropbox_url():
    for dir_url in DROPBOX_DIR_URL:
        for i in BeautifulSoup(get_web_document(dir_url['URL']), 'html.parser'):
            if isinstance(i, bs4.element.Tag):
                for j in i.text.splitlines():
                    if 'function (mod, InitReact)' in j:
                        json_item = j.split('mod', 2)[2][2:].rsplit(')', 3)[0]
                        compare_local_vs_dropbox(json.loads(json_item)['props']['contents']['files'], dir_url['DIR'])
                        break


if __name__ == '__main__':
    parse_dropbox_url()
