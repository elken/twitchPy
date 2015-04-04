#!/usr/bin/env python3
import sys
from gi.repository import Gtk, WebKit2
from urllib.parse import parse_qs

class Browser(Gtk.Window):
    def __init__(self, uri):
        Gtk.Window.__init__(self, title="Web browser")

        webview = WebKit2.WebView()
        webview.load_uri(uri)
        webview.connect("load-changed", self.printUri)
        self.add(webview)
        self.set_default_size(800, 600)
        
    def returnToken(self):
        return self.token 

    def printUri(self, view, state):
        if state is WebKit2.LoadEvent.REDIRECTED:
            uri = view.get_uri()
            pUri = parse_qs(view.get_uri())
            try: 
                pUri['http://localhost/#access_token']
            except KeyError:
                print("Not found")
            else:
                self.token = pUri['http://localhost/#access_token']
                Gtk.main_quit
                print(self.token)
                sys.exit()



b = Browser('https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=li1pr10xcvzh6mmkudjjmlcrt0i7uz9&redirect_uri=http://localhost&scope=user_follows_edit')
b.connect("delete-event", Gtk.main_quit)
b.show_all()
Gtk.main()
