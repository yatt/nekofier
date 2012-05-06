# coding: utf-8
import urllib
import re

def link():
    # nekostagramからデータを取得
    conn = urllib.urlopen('http://nekostagram.heroku.com/')
    cont = conn.read(4096)
    # 画像リンクのみ抽出
    lst = re.findall(r'(http://dist.+?\.jpg)["\']', cont)
    return lst[0]
