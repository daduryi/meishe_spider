import json
import os

import requests

from .meishe_token import g_token
from model.spider_log import log_msg
from model.util import save_file, ua, parse_raw_header


class MsUserSpider(object):

    base_dir = os.path.join(os.path.dirname(__file__), 'data')

    _html_url = 'https://m.meisheapp.com/person/index.html?id='

    VIDEO_LIST_JSON = 'video_list.json'

    def log_msg(self, msg):
        log_msg(f'[{self.user_id}] {msg}')

    def __init__(self, user_id):
        self.user_id = user_id
        self.html_url = self._html_url + str(user_id)
        self.user_dir = os.path.join(self.base_dir, str(user_id))
        self.local_html = os.path.join(self.user_dir, 'index.html')
        self.local_detail = os.path.join(self.user_dir, 'detail.json')
        self.local_share_info = os.path.join(self.user_dir, 'share_info.json')
        self.local_video_list = os.path.join(self.user_dir, self.VIDEO_LIST_JSON)
        self.local_done = os.path.join(self.user_dir, 'done.txt')

    def prepare(self):
        if not os.path.exists(self.user_dir):
            os.mkdir(self.user_dir)

    def request_html(self):
        header = parse_raw_header('''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: en,zh-CN;q=0.9,zh;q=0.8
        cache-control: no-cache
        cookie: accessToken_pro={token}
        pragma: no-cache
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        sec-fetch-user: ?1
        upgrade-insecure-requests: 1
        user-agent: {ua}
        '''.format(ua=ua, token=self.token))

        response = requests.get(self.html_url, headers=header)
        self.log_msg(f'request html {self.html_url} {response.status_code}')
        return response.status_code == 200, response.content.decode('utf8')

    def request_detail(self):
        header = parse_raw_header(f'''
        Accept: */*
        Accept-Encoding: gzip, deflate, br
        Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
        Cache-Control: no-cache
        Connection: keep-alive
        Host: api.meisheapp.com
        Origin: https://m.meisheapp.com
        Pragma: no-cache
        Referer: {self.html_url}
        Sec-Fetch-Dest: empty
        Sec-Fetch-Mode: cors
        Sec-Fetch-Site: same-site
        user-agent: {ua}
        ''')

        url = f'https://api.meisheapp.com/v1/user/detail?query_user_id={self.user_id}&token=&user_id=&access_token={self.token}'
        response = requests.get(url, headers=header)
        self.log_msg(f'request detail {url} {response.status_code}')
        return response.status_code == 200, response.json()

    def request_share_info(self):
        # url = 'https://api.meisheapp.com/v1/weixin/getShareInfo?url=https%253A%252F%252Fm.meisheapp.com%252Fperson%252Findex.html%253Fid%253D2810203&access_token=AF90AF12121C2368209154ACB0A0F5DB'
        pass

    def get_start_id(self):
        start_ids = sorted([int(e.split('.')[0].split('_')[-1]) for e in os.listdir(self.user_dir) if e.startswith('video_') and e.endswith('.json')])
        if start_ids:
            return start_ids[0]
        return 0

    def get_video_nums(self):
        return len([int(e.split('.')[0].split('_')[-1]) for e in os.listdir(self.user_dir) if e.startswith('video_') and e.endswith('.json')])

    def request_video_list(self):
        header=parse_raw_header(f'''
        Accept: */*
        Sec-Fetch-Dest: empty
        User-Agent: {ua}
        Origin: https://m.meisheapp.com
        Sec-Fetch-Site: same-site
        Sec-Fetch-Mode: cors
        Referer: {self.html_url}
        Accept-Encoding: gzip, deflate, br
        Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
        ''')
        start_id=self.get_start_id()
        url=f'https://community.meisheapp.com/meishe/user/?queryUserId={self.user_id}&command=getUserFilmList&token=&userId=&maxNum=10&startId={start_id}'
        response=requests.get(url, headers = header)
        self.log_msg(f'request videos {url} {response.status_code}')
        return response.status_code == 200, response.json()

    def is_done(self):
        return os.path.exists(self.local_done)

    def mark_done(self, msg):
        save_file(self.local_done, msg)

    @property
    def token(self):
        return g_token.get_token(self.user_id)

    def parse_userinfo(self):
        pass

    def save_html(self, text):
        save_file(self.local_html, text)

    def save_detail(self, data):
        save_file(self.local_detail, json.dumps(data))

    def save_share_info(self, data):
        save_file(self.local_share_info, json.dumps(data))

    def save_video_list(self, startid, data):
        save_file(f'{self.local_video_list}.{startid}', json.dumps(data))
