import time
import requests
import json 
import os

from model.spider_error import ResponseError
from model.spider_log import log_msg
from model.util import parse_raw_header


class TokenModel(object):

    client_id = 'msd0c28f00413d6c95'

    secret = 'a89c4996d0c28f00413d6c95ff6e4a2a'

    token_path = os.path.join(os.path.dirname(__file__), 'data/.token.json')

    token_url = f'https://api.meisheapp.com/accessToken?client_id={client_id}&secret={secret}'

    def __init__(self):
        self._token, self._expire_at = self.load_cache_token()

    def refresh_token(self, user_id):
        headers = parse_raw_header('''
        Host: api.meisheapp.com
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0
        Accept: */*
        Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
        Accept-Encoding: gzip, deflate, br
        Origin: https://m.meisheapp.com
        Connection: keep-alive
        Referer: https://m.meisheapp.com/person/index.html?id={user_id}
        Pragma: no-cache
        Cache-Control: no-cache
        '''.format(user_id=user_id))

        response = requests.get(self.token_url, headers=headers)
        if response.status_code != 200:
            raise ResponseError('not 200')

        data = response.json()
        if data['errNo'] != 0:
            raise ResponseError('errNo not 0')

        return data['access_token'], data['expires']

    def set_token(self, token, expire_at):
        self._token = token
        self._expire_at = expire_at

    def cache_token(self):
        with open(self.token_path, 'w') as f:
            json.dump({'token': self._token, 'expire_at': self._expire_at}, f)

    def load_cache_token(self):
        if os.path.exists(self.token_path):
            with open(self.token_path) as f:
                d = json.load(f)
                return d['token'], d['expire_at']
        return None, None

    def get_token(self, user_id):
        if not self._token or self._expire_at - time.time() > 100:
            self.set_token(*self.refresh_token(user_id))
            self.cache_token()
            log_msg(f'refresh token success: {self._token} {self._expire_at}')
        return self._token


g_token = TokenModel()
