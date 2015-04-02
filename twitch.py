#!/usr/bin/env python3
import math
import os
import errno
import json
import requests
import gui
import tempfile
import posixpath 
import timeit
import fnmatch

try:
    from shlex import quote 
except ImportError:
    from pipes import quote

from collections import OrderedDict
from threading import Thread 
from queue import Queue
from gi.repository import Gtk

USER = "altf4towin"
TOKEN_URL = 'https://api.twitch.tv/kraken/users/' + USER + '/follows/channels'

class Twitch():
    def __init__(self):
        self.j = self.getJSON(limit=1)

        self.data = json.loads(self.j)
        self.limit = self.data["_total"]
        self.follows = []
        self.iUrls = {}
        self.rDict = {}
        self.imageQueue = Queue()
        self.rQueue = Queue()

        ub = 10
        ub1,ub2 = divmod(self.limit, ub)
        while len(str(ub1)) is not 1:
            ub=ub*10
            ub1,ub2 = divmod(self.limit, ub)

        s=0
        i=1
        n=self.limit

        while(n>=0):
            a,b = divmod(n, ub)
            if a is not 0:
                self.rQueue.put(a*ub)
            else:
                self.rQueue.put(b)
            self.rQueue.put(s)
            self.rQueue.put(i)
            s=s+100
            i=i+1
            n=n-100

        for i in range(5):
            t = Thread(target=self.getFollows)
            t.daemon = True
            t.start()
        
        self.rQueue.join()
        self.createTempDir()

    def getFollows(self):
        while True:
            limit = self.rQueue.get()
            offset = self.rQueue.get()
            i = self.rQueue.get()

            self.rDict[i] = self.getJSON(limit=limit, offset=offset)

            self.rQueue.task_done()
            self.rQueue.task_done()
            self.rQueue.task_done()

    def getJSON(self, limit=100, offset=0):
        r = requests.get(TOKEN_URL, params={'limit': limit,'offset': offset})
        if r.status_code is 200:
            return json.dumps(r.json())
        else:
            print("Error getting JSON from " + TOKEN_URL + ". Check network settings. (" + str(r.status_code) +")")

    def createTempDir(self):
        try:
            self.tempDir
        except AttributeError:
            flag = False
            for i in os.listdir(tempfile.gettempdir()):
                if fnmatch.fnmatch(i, 'twitchpy_*'):
                    flag = True
                    break

            if flag:
                self.tempDir = os.path.join(tempfile.gettempdir(), i)
            else:
                self.tempDir = tempfile.mkdtemp(prefix="twitchpy_")

            print(("Using '" + self.tempDir + "' as temp dir."))

    def getImage(self):
        while True:
            url = self.imageQueue.get()
            s = posixpath.basename(url)

            print("Trying " + url)
            try:
                with open(s) as file:
                    pass 
            except IOError:
                image = open(s, 'wb')
                image.write(requests.get(quote(url)).content)
                image.close()
            self.imageQueue.task_done()

    def downloadLogos(self):
        try:
            self.iUrls
        except KeyError as NameError:
            print("Error accessing image URLs")
            pass
        else:
            for i in self.iUrls.values():
                self.imageQueue.put(i)

            for i in range(15):
                t = Thread(target=self.getImage)
                t.daemon = True 
                t.start()

            self.imageQueue.join()

    def parseFollows(self):
        for i in self.rDict:
            f = json.loads(self.rDict[i])
            for j in f['follows']:
                self.follows.append(json.dumps(j['channel']['display_name']).strip('"'))

        self.follows.sort(key=lambda s: s.lower())

    def parseImageURL(self):
        if self.follows:
            self.iUrls.fromkeys(self.follows)

        for i in self.rDict:
            u = json.loads(self.rDict[i])
            for j in u['follows']:
                if json.dumps(j['channel']['logo']).strip('"') is not "null":
                    self.iUrls[json.dumps(j['channel']['display_name'])] = (json.dumps(j['channel']['logo']).strip('"')).replace("300x300", "150x150")
                else:
                    self.iUrls[json.dumps(j['channel']['display_name'])] = "http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png"

        self.iUrls = OrderedDict(sorted(list(self.iUrls.items()), key=lambda s: s[0].lower()))

    def getLogos(self):
        try:
            os.chdir(self.tempDir)
        except AttributeError:
            print("Temp dir not created yet")
        self.downloadLogos()

    def printFollows(self):
        for i in self.follows:
            print(i)
    
    def printLogos(self):
        for i, j in list(self.iUrls.items()):
            print((i, j))

    def returnFollows(self):
        return self.follows

    def returnImageURL(self):
        return self.iUrls

    def returnJSON(self):
        return self.rDict

    def returnTempDir(self):
        return self.tempDir


if __name__ == '__main__':
    #print(timeit.timeit("t = TObj()", setup="from __main__ import TObj", number=1))
    #t = Twitch()
    #t.parseFollows()
    #t.printFollows()
    g = gui.MainWindow()
    g.run()
    #t.parseImageURL()
    #t.getLogos()
    #t.printLogos()
