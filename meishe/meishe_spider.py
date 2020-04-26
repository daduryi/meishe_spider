# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 11:15 上午
# @Author  : lixn
import time

from .meishe_user import MsUserSpider
from .meishe_video import MsVideoSpider
from model.spider_log import log_msg


class MsSpider(object):

    @staticmethod
    def fetch(user_id, max_video_num=None):

        meishe = MsUserSpider(user_id)
        if meishe.is_done():
            meishe.log_msg('is done!')
            return

        meishe.prepare()
        success, text = meishe.request_html()
        meishe.save_html(text)
        _, detail = meishe.request_detail()
        meishe.save_detail(detail)
        while True:
            start_id = meishe.get_start_id()
            meishe.log_msg(f'next page. user_id: {meishe.user_id} user_dir: {meishe.user_dir} start_id: {start_id}')
            success, data = meishe.request_video_list()
            video_list = data['list']
            for video in video_list:
                vspider = MsVideoSpider(video, meishe)
                time.sleep(1)
                vspider.request_file()
                vspider.save_data()

            meishe.save_video_list(start_id, data)

            if max_video_num is not None and meishe.get_video_nums() >= max_video_num:
                meishe.log_msg('had max_video_numbers end!')
                meishe.mark_done(str(meishe.get_video_nums()))
                break

            if not video_list:
                meishe.log_msg(f'request videos {meishe.user_id} end')
                meishe.mark_done('end')
                break
