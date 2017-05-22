#-*- coding: utf-8 -*-

from validator import Validator


class ElemeSpider(Validator):
    name = 'eleme'
    concurrent_requests = 8

    def __init__(self, name = None, **kwargs):
        super(ElemeSpider, self).__init__(name, **kwargs)

        self.urls = [
            'https://mainsite-restapi.ele.me/shopping/restaurants?latitude=31.27213&longitude=121.61479&limit=1'
        ]

        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

        self.success_mark = '[{'
        self.is_record_web_page = False
        self.init()
