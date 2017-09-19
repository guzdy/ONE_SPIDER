# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class UAMiddleware(UserAgentMiddleware):
    class RotateUserAgentMiddleware(UserAgentMiddleware):
        def process_request(self, request, spider):
            ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            print("********Current UserAgent:%s************" % ua)
            request.headers.setdefault('User-Agent', ua)