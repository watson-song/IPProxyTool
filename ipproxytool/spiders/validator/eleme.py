#-*- coding: utf-8 -*-

import random
import time

from scrapy import Request

import config
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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'mainsite-restapi.ele.me',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
        }

        self.success_mark = '[{'
        self.is_record_web_page = False

        self.init()

    def start_requests(self):
        count = self.sql.get_proxy_count(self.name)
        count_httpbin = self.sql.get_proxy_count(config.httpbin_table)

        ids = self.sql.get_proxy_ids(self.name)
        ids_httpbin = self.sql.get_proxy_ids(config.httpbin_table)

        for i in range(0, count + count_httpbin):
            table = self.name if (i < count) else config.httpbin_table
            id = ids[i] if i < count else ids_httpbin[i - len(ids)]

            proxy = self.sql.get_proxy_with_id(table, id)
            if proxy is None:
                continue

            url = random.choice(self.urls)

            cur_time = time.time()
            yield Request(
                    url=url,
                    headers=self.headers,
                    meta={
                        'cur_time': cur_time,
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'proxy': 'http://%s:%s' % (proxy.ip, proxy.port),
                    },
                    dont_filter=True,
                    callback=self.success_parse,
                    errback=self.error_parse
            )