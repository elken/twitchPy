import concurrent
import json
import os
from concurrent.futures import ThreadPoolExecutor
from os.path import basename
from queue import Queue
from threading import Thread

from Request import *


class Twitch:

    def __init__(self, temp_dir):
        self.temp_dir = temp_dir
        self.json = get_json("altf4towin", "/follows/channels/", limit=1)
        self.data = json.loads(self.json)
        self.follows = []
        self.image_urls = {}
        self.req_dict = {}
        self.image_queue = Queue()
        self.req_queue = Queue()
        self.limit = self.data['_total']

        upper_bound = 10
        new_bound, ub2 = divmod(self.limit, upper_bound)
        while len(str(new_bound)) is not 1:
            upper_bound *= 10
            new_bound, ub2 = divmod(self.limit, upper_bound)
        
        offset = 0
        counter = 1
        new_limit = self.limit

        with ThreadPoolExecutor(max_workers=(os.cpu_count())) as e:
            while new_limit >= 0:
                quotient, remainder = divmod(new_limit, upper_bound)
                if quotient is not 0:
                    limit = (quotient * upper_bound)
                else:
                    limit = remainder
                offset = offset
                counter = counter

                offset += 100
                counter += 1
                new_limit -= 100

                f = e.submit(self.get_follows, limit, offset, counter)
                self.req_dict[counter] = f.result()

        self.req_queue.join()
        self.parse_follows()
        print(self.follows)
        self.get_image_urls()
        self.download_images()
        # for i, j in self.image_urls.items():
        #     print(i, j)
        # for i in self.req_dict:
        #     item = json.loads(self.req_dict[i])
        #     for j in item['follows']:
        #         print(json.dumps(j['channel'], sort_keys=True, indent=4))

    @staticmethod
    def get_follows(limit=None, offset=None, counter=None):
            return get_json("altf4towin", "/follows/channels", limit=limit, offset=offset)

    def parse_follows(self):
        for i in self.req_dict:
            item = json.loads(self.req_dict[i])
            for j in item['follows']:
                self.follows.append(json.dumps(j['channel']['display_name'].strip('""')))

        self.follows.sort(key=lambda s: s.lower())

    def get_image_urls(self):
        if self.follows:
            self.image_urls.fromkeys(self.follows)

        for i in self.req_dict:
            item = json.loads(self.req_dict[i])
            for j in item['follows']:
                logo_name = json.dumps(j['channel']['logo'])
                name = json.dumps(j['channel']['display_name'])
                if logo_name is not "null":
                    self.image_urls[name] = logo_name.strip('"').replace("300x300", "150x150")
                else:
                    self.image_urls[name] = "http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png"

    def download_images(self):
        with ThreadPoolExecutor(max_workers=(os.cpu_count())) as e:
            f_url = {e.submit(self.download_image, url): url for url in self.image_urls.values()}
            for f in concurrent.futures.as_completed(f_url):
                url = f_url[f]
                name = basename(url)
                file_path = os.path.join(self.temp_dir, name)
                if not os.path.exists(file_path):
                    print('Trying {}'.format(url))
                    try:
                        data = f.result()
                        with open(file_path, 'wb') as file:
                            file.write(data)
                    except Exception as ex:
                        print('Threw exception {}'.format(ex))
                        pass

    @staticmethod
    def download_image(url):
        if url is not "null":
            return requests.get(url).content
