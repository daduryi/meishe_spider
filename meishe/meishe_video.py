import json
import os

import requests

from .meishe_token import g_token
from model.util import parse_raw_header, save_bfile
from model.util import save_file, ua, parse_raw_header


class MsVideoSpider(object):

    def __init__(self, data, meishe):
        self.meishe = meishe
        self.data = data
        self.asset_id = data['assetId']
        self.publish_url = data['publishUrl']
        self.video_url = data['filmUrl']
        self.logo_url = data['thumbUrl'].split('?')[0]
        self.request_url = self.publish_url
        self.local_video = os.path.join(self.meishe.user_dir, f'video_{self.asset_id}.mp4')
        self.local_image = os.path.join(self.meishe.user_dir, f'video_{self.asset_id}.jpg')
        self.local_json = os.path.join(self.meishe.user_dir, f'video_{self.asset_id}.json')
        '''
        assetId : "22064767"
        filmUrl : "http://meishevideo.meisheapp.com/transvideo/2020/04/13/task-1-CB1AB08F-0A83-D620-40A8-D1638479CCB7.mp4"
        thumbUrl : "http://meishevideo.meisheapp.com/thumbnail/2020/04/13/task-1-CB1AB08F-0A83-D620-40A8-D1638479CCB7.jpg?imageView2/2/w/600"
        filmDesc : "四月春意正浓（2）"
        viewsCount : 5218
        praiseCount : 225
        commentCount : 433
        publishDate : "2020-04-13 08:13:36"
        publishUrl : "https://m.meisheapp.com/share/index_9.html?id=22064768"
        isPublic : 1
        assetFlag : 20
        fileLength : 194889755
        hasPraised : false
        hasRecommend : false
        themeType : 0
        giftCount : "31"
        sceneFlag : 0
        '''

    @property
    def token(self):
        return g_token.get_token(self.meishe.user_id)

    def request_video_html(self):
        headers = parse_raw_header(f'''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: en,zh-CN;q=0.9,zh;q=0.8
        cache-control: no-cache
        pragma: no-cache
        referer: {self.meishe.html_url}
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: same-origin
        sec-fetch-user: ?1
        upgrade-insecure-requests: 1
        user-agent: {ua}
        ''')
        r = requests.get(self.publish_url, headers=headers)
        self.request_url = r.request.url
        return r.status_code == 200, r.content.decode('utf8')

    def request_video_index(self):
        headers = parse_raw_header(f"""
        Connection: keep-alive
        Pragma: no-cache
        Cache-Control: no-cache
        Accept: */*
        Sec-Fetch-Dest: empty
        User-Agent: {ua}
        Origin: https://m.meisheapp.com
        Sec-Fetch-Site: same-site
        Sec-Fetch-Mode: cors
        Referer: {self.request_url}
        Accept-Encoding: gzip, deflate, br
        Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
        """)
        url = f'https://api.meisheapp.com/v1/asset/index?asset_id={self.asset_id}&access_token={self.token}&need_ch=1&is_first=0&need_gif=1'
        r = requests.get(url, headers=headers)
        return r.status_code, r.json()

    # def request_file(self, data):
    #     headers = parse_raw_header(f"""
    #     Accept: */*
    #     User-Agent: {ua}
    #     Accept-Language: zh-cn
    #     Accept-Encoding: identity
    #     Connection: Keep-Alive
    #     """)
    #     r = requests.get(data['file_url'], headers=headers)
    #     save_file(self.local_video, r.content)
    #
    #     r = requests.get(data['thumb_file_url'], headers=headers)
    #     save_file(self.local_video, r.content)

    def save_data(self):
        save_file(self.local_json, json.dumps(self.data))

    def request_file(self):
        headers = parse_raw_header(f"""
        Accept: */*
        User-Agent: {ua}
        Accept-Language: zh-cn
        Accept-Encoding: identity
        Connection: Keep-Alive
        """)
        self.meishe.log_msg(f'download {self.video_url} -> {self.local_video}')
        r = requests.get(self.video_url, headers=headers)
        save_bfile(self.local_video, r.content)

        self.meishe.log_msg(f'download {self.logo_url} -> {self.local_image}')
        r = requests.get(self.logo_url, headers=headers)
        save_bfile(self.local_image, r.content)
