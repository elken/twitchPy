import json

import requests


def get_json(user, route="", limit=100, offset=0):
    r = requests.get('https://api.twitch.tv/kraken/users/' + user + route, params={'limit': limit, 'offset': offset})
    if r.status_code is 200:
        return json.dumps(r.json())
    else:
        raise requests.RequestException("Error getting JSON from " + r.url + ". Check network connection.")

