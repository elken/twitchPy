import concurrent.futures
import os

from Request import *


class Twitch:
    def __init__(self, temp_dir, settings):
        self.settings = settings
        self.temp_dir = temp_dir
        self.acc_name = self.settings.value("name")
        self.json = get_json(self.acc_name, "/follows/channels/", limit=1)
        self.limit = json.loads(self.json)['_total']
        self.following = {}

        self.process_follows()
        self.download_images()

    def download_images(self):
        with concurrent.futures.ThreadPoolExecutor() as e:
            url_dict = {e.submit(lambda: requests.get(url).content): url
                        for url in [x for x in self.following.values()
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

    def process_follows(self):
        # Figure out how many requests we need to make
        upper_bound = 10
        new_bound, ub2 = divmod(self.limit, upper_bound)
        while len(str(new_bound)) is not 1:
            upper_bound *= 10
            new_bound, ub2 = divmod(self.limit, upper_bound)

        offset = 0
        counter = 1
        new_limit = self.limit

        with concurrent.futures.ThreadPoolExecutor() as e:
            # Use division to figure out the correct limit of requests, ie when the limit is <100
            while new_limit >= 0:
                quotient, remainder = divmod(new_limit, upper_bound)
                if quotient is not 0:
                    limit = (quotient * upper_bound)
                else:
                    limit = remainder

                f = e.submit(get_json, self.acc_name, "/follows/channels", limit, offset)
                json_data = json.loads(f.result())

                self.following.update(
                        {key: value for (key, value) in
                         ((j['channel']['display_name'],
                           str(j['channel']['logo']).replace("300x300", "150x150").replace(
                                   "None",
                                   "http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png"))
                          for j in json_data['follows'])})

                offset += 100
                counter += 1
                new_limit -= 100
