import concurrent.futures
import os

from Request import *

MAX_THREADS = os.cpu_count() + 1


class Twitch:
    def __init__(self, temp_dir, settings):
        self.settings = settings
        self.temp_dir = temp_dir
        self.acc_name = self.settings.value("name")
        self.json = get_json(self.acc_name, "/follows/channels/", limit=1)
        self.data = json.loads(self.json)
        self.follows = []
        self.image_urls = {}
        self.req_dict = {}
        self.limit = self.data['_total']

        self.calc_bounds()

        self.parse_follows()
        self.get_image_urls()
        self.download_images()
        # for i, j in self.image_urls.items():
        #     print(i, j)
        # for i in self.req_dict:
        #     item = json.loads(self.req_dict[i])
        #     for j in item['follows']:
        #         print(json.dumps(j['channel'], sort_keys=True, indent=4))

    def get_follows(self, limit=None, offset=None):
        return get_json(self.acc_name, "/follows/channels", limit=limit, offset=offset)

    def parse_follows(self):
        for i in self.req_dict:
            item = json.loads(self.req_dict[i])
            self.follows += ([j['channel']['display_name'] for j in item['follows']])
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as e:
            url_dict = {e.submit(self.download_image, url): url
                        for url in [x for x in self.image_urls.values()
                                    if not os.path.exists(os.path.join(self.temp_dir, os.path.basename(x)))]}
            for url_content in concurrent.futures.as_completed(url_dict):
                url = url_dict[url_content]
                name = os.path.basename(url)
                file_path = os.path.join(self.temp_dir, name)
                if not os.path.exists(file_path):
                    print('Trying {}'.format(url))
                    try:
                        data = url_content.result()
                        with open(file_path, 'wb') as file:
                            file.write(data)
                    except Exception as ex:
                        print('Threw exception {}'.format(ex))
                        pass

    @staticmethod
    def download_image(url):
        if url is not "null":
            return requests.get(url).content

    def calc_bounds(self):
        # Figure out how many requests we need to make
        upper_bound = 10
        new_bound, ub2 = divmod(self.limit, upper_bound)
        while len(str(new_bound)) is not 1:
            upper_bound *= 10
            new_bound, ub2 = divmod(self.limit, upper_bound)

        offset = 0
        counter = 1
        new_limit = self.limit

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as e:
            # Use division to figure out the correct limit of requests, ie when the limit is <100
            while new_limit >= 0:
                quotient, remainder = divmod(new_limit, upper_bound)
                if quotient is not 0:
                    limit = (quotient * upper_bound)
                else:
                    limit = remainder

                f = e.submit(self.get_follows, limit, offset)
                self.req_dict[counter] = f.result()

                offset += 100
                counter += 1
                new_limit -= 100
