#!/usr/bin/env python
import os
import json
import requests
import gui
import requests.packages.urllib3.contrib.pyopenssl
import tempfile
import collections

USER = "altf4towin"
TOKEN_URL = 'https://api.twitch.tv/kraken/users/' + USER + '/follows/channels'

class TObj():

    def __init__(self):
        self.r = requests.get(TOKEN_URL, params={'limit': '100','verify': 'True'})
        self.j = json.dumps(self.r.json(), sort_keys=True, indent=4, separators=(',',':'))

        self.data = json.loads(self.j)
        self.limit = self.data["_total"]
        self.follows = []
        self.iUrls = {}

        while(self.limit >= 0):
            s=0
            i=1
            self.rDict = {}

            while(self.limit >= 0):
                if(self.limit <= 100):
                    self.r = requests.get(TOKEN_URL, params={'limit': self.limit, 'offset': s,'verify': 'True'})
                    self.rDict[i] = json.dumps(self.r.json(), indent=4, separators=(',',':'))

                    self.limit=0

                self.r = requests.get(TOKEN_URL, params={'limit': '100', 'offset': s,'verify': 'True'})
                self.rDict[i] = json.dumps(self.r.json(), indent=4, separators=(',',':'))

                self.limit = self.limit - 100
                s=s+100
                i=i+1

        self.createTempDir()

    def createTempDir(self):
        try:
            type(self.tempDir) is str
        except AttributeError:
            self.tempDir = tempfile.mkdtemp(prefix="twitchpy_")
            print("Using '" + self.tempDir + "' as temp dir.")

    def downloadLogos(self):
        try:
            self.iUrls[1]
        except KeyError, NameError:
            print("Error accessing image URLs")
        else:
            for i in self.iUrls:
                if i:
                    if i is not "null":
                        print("Trying "+i)
                        image = open(i[46:], 'wb')
                        image.write(requests.get(i).content)
                        image.close()

    def getFollows(self):
        for i in self.rDict:
            f = json.loads(self.rDict[i])
            for j in f['follows']:
                self.follows.append(json.dumps(j['channel']['display_name']).strip('"'))

        self.follows.sort(key=lambda s: s.lower())

    def getImageURL(self):
        if self.follows:
            self.iUrls.fromkeys(self.follows)

        for i in self.rDict:
            u = json.loads(self.rDict[i])
            for j in u['follows']:
                self.iUrls[json.dumps(j['channel']['display_name'])] = (json.dumps(j['channel']['logo']).strip('"'))

        self.iUrls = collections.OrderedDict(sorted(self.iUrls.items(), key=lambda s: s[0].lower()))

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
        for i, j in self.iUrls.items():
            print(i, j)

#g = gui.MainWindow()
#g.run()
requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()
t = TObj()

t.getFollows()
t.getImageURL()
t.printLogos()
#t.getLogos()
