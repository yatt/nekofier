# coding: utf-8
import urllib
import urllib2
import re
import json

def get():
    return get_20130428()

def get_20130428():
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('Accept-Language', 'Accept-Language:ja,en-US;q=0.8,en;q=0.6'),
        ('Accept', 'application/json, text/javascript, */*; q=0.01'),
        ('X-Requested-With', 'XMLHttpRequest'),
        ]
    conn = opener.open('http://nekostagram.heroku.com/')
    js = json.load(conn)
    urllist = [data['images']['low_resolution']['url'] for data in js['data']]
    return urllist[0]

def get_before_20130428():
    # nekostagramからデータを取得
    conn = urllib.urlopen('http://nekostagram.heroku.com/')
    cont = conn.read(4096)
    # 画像リンクのみ抽出
    lst = re.findall(r'(http://dist.+?\.jpg)["\']', cont)
    return lst[0]


if __name__ == '__main__':
    print get()
