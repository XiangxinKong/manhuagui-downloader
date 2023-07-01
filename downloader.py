# @Author: Xiangxin Kong
# @Date: 2020.5.30
import requests
import re
import os
import time
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from decoder import get
from header import header


class MangaDownloader:
    def __init__(self, address, path):
        self.path = path + "/"
        self.baseURL = "https://www.manhuagui.com"
        url = "https://www.manhuagui.com/comic/" + re.match(r'^.*comic/([0-9]+)/?', address).group(1)
        self.getAbstraction(url)


    def getAbstraction(self, url):
        req = requests.get(url).content
        bf = BeautifulSoup(req, 'html.parser')

        self.title = bf.h1.text
        self.author = bf.find("strong", text="漫画作者：").parent.a.text
        self.plot = bf.find("strong", text="漫画剧情：").parent.a.text
        self.year = bf.find("strong", text="出品年代：").parent.a.text
        self.region = bf.find("strong", text="漫画地区：").parent.a.text
        self.chapters = list(
            map(lambda x: [x.get('title'), x.get('href'), None], bf.find_all('a',{'class':'status0'})))
        self.chapters.reverse()
        self.length = len(self.chapters)

    def existedChapters(self):
        """return a list of Chapters<String> that already existed"""
        localChapters = []
        for chapter in self.chapters:
            if os.path.isdir(self.path + self.title + "/" + chapter[0]):
                localChapters.append(chapter[0])
        return localChapters

    @staticmethod
    def createDirectory(path):
        """create a new file at path"""
        print("create")
        Path(path).mkdir(parents=True, exist_ok=True)

    def isMangaExist(self):
        """return true if the manga already existed"""
        return os.path.isdir(self.path + self.title + "/")

    def downloadChapter(self, url):
        abstraction = get(self.baseURL + "/" + url)
        mangaName = abstraction['bname']
        chapterName = abstraction['cname']
        length = abstraction['len']
        e = abstraction['sl']['e']
        m = abstraction['sl']['m']
        path = abstraction['path']

        localPath = self.path + "/" + mangaName + "/" + chapterName + "/"
        self.createDirectory(localPath)
        print('下载 %s %s 中 共%s页' % (mangaName, chapterName, length))

        for filename in abstraction['files']:
            pgUrl = 'https://i.hamreus.com' + path + filename
            print(os.path.basename(pgUrl))
            self.downloadPg(pgUrl, e, m, localPath)
            time.sleep(0.5)  # 0.5s interval
        return True

    def downloadPg(self, url, e, m, localPath):
        # repeat 10 times
        for i in range(10):
            try:
                res = requests.get(url, params={'e': e, 'm': m}, headers=header, timeout=10)
                res.raise_for_status()
            except:
                print('页面 %s 下载失败 重试中...' % url)
                print('等待2秒...')
                # wait for 2s
                time.sleep(2)
                continue
            filename = (localPath + os.path.basename(url))[:-5]
            file = open(filename, 'wb')
            file.write(res.content)
            file.close()
            # transfer to jpg
            Image.open(filename).save(filename, 'jpeg')
            return
        print('超过重复次数 跳过此章')

