#!/usr/bin/env python2
import json
import requests
from pprint import pprint

class TObj(self):

    def __init__(self):
        self.r = requests.get("https://api.twitch.tv/kraken/users/altf4towin/follows/channels")
        self.j = json.dumps(self.r.json(), sort_keys=True, indent=4, separators=(',',':'))

        self.data = json.load(self.j)
        pprint(self.data)


    def printJSON(self):
        print self.j
