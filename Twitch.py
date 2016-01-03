import concurrent.futures
import os
import urllib.request

import workerpool

from Request import *


class Twitch:
    def __init__(self, temp_dir, settings):
        self.settings = settings
        self.temp_dir = temp_dir
        self.acc_name = self.settings.value('name')
        self.following = {}

        self.process_follows()
        self.download_images()

    def download_images(self):
        pool = workerpool.WorkerPool(size=os.cpu_count() * 5)
        urls = [x for x in self.following.values()
                if not os.path.exists(os.path.join(self.temp_dir, os.path.basename(x)))]
        file_path = [os.path.join(self.temp_dir, os.path.basename(url)) for url in urls]

        pool.map(self.download_image, urls, file_path)
        pool.shutdown()
        pool.wait()

    @staticmethod
    def download_image(url, path):
        print('Trying {}'.format(url))
        urllib.request.urlretrieve(url, path)

    def process_follows(self):
        # Figure out how many requests we need to make
        req = json.loads(get_json(self.acc_name, '/follows/channels/'))
        limit = req['_total']
        self.following.update(
                {key: value for (key, value) in
                 ((j['channel']['display_name'],
                   str(j['channel']['logo']).replace('300x300', '150x150').replace(
                           'None',
                           'http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png'))
                  for j in req['follows'])})

        if limit > 100:
            upper_bound = 10
            new_bound, ub2 = divmod(limit, upper_bound)
            while len(str(new_bound)) is not 1:
                upper_bound *= 10
                new_bound, ub2 = divmod(limit, upper_bound)

            offset = self.following.__len__() + 1
            counter = 2
            new_limit = limit

            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 5) as e:
                # Use division to figure out the correct limit of requests, ie when the limit is <100
                if new_limit >= 0:
                    quotient, remainder = divmod(new_limit, upper_bound)
                    if quotient is not 0:
                        limit = (quotient * upper_bound)
                    else:
                        limit = remainder

                    f = e.submit(get_json, self.acc_name, '/follows/channels', limit, offset)
                    json_data = json.loads(f.result())

                    self.following.update(
                            {key: value for (key, value) in
                             ((j['channel']['display_name'],
                               str(j['channel']['logo']).replace('300x300', '150x150').replace(
                                       'None',
                                       'http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png'))
                              for j in json_data['follows'])})

                    offset += 100
                    counter += 1
                    new_limit -= 100
