#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import dns.resolver
import urllib
from urllib.parse import urlparse

class CdnCheck(object):
    def __init__(self, url):
        super(CdnCheck, self).__init__()
        self.cdninfo()
        self.url = url
        self.cnames = []
        self.headers = []

    def get_cnames(self): # get all cname
        furl = urllib.parse.urlparse(self.url)
        url = furl.netloc
        # print url

        rsv = dns.resolver.Resolver()
        # rsv.nameservers = ['114.114.114.114']
        try:
            answer = dns.resolver.query(url,'CNAME')
        except Exception as e:
            self.cnames = None
            # print "ERROR: %s" % e
        else:
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)

    def get_cname(self,cname): # get cname
        try:
            answer = dns.resolver.query(cname,'CNAME')
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)
        except dns.resolver.NoAnswer:
            pass

    def get_headers(self): # get header
        try:
            resp = urllib.urlopen(self.url)
        except Exception as e:
            self.headers = None
            # print "ERROR: %s" % e
        else:
            headers = str(resp.headers).lower()
            self.headers = headers

    def matched(self, context, *args): # Matching string
        if not isinstance(context, basestring):
            context = str(context)

        func = lambda x, y: y in x
        for pattern in args:
            if func(context,pattern):
                return pattern
        return False

    def check(self):
        flag = None
        self.get_cnames()
        self.get_headers()
        if self.cnames:
            # print self.cnames
            flag = self.matched(self.cnames,*self.cdn['cname'])
            if flag:
                return {'Status':True, 'CDN':self.cdn['cname'].get(flag)}
        if not flag and self.headers:
            flag = self.matched(self.headers,*self.cdn['headers'])
            if flag:
                return {'Status':True, 'CDN':'unknown'}
        return {'Status':False, 'CNAME':self.cnames, 'Headers':self.headers}

    def cdninfo(self):
        self.cdn = {
            'headers': set([
                'via',
                'x-via',
                'by-360wzb',
                'by-anquanbao',
                'cc_cache',
                'cdn cache server',
                'cf-ray',
                'chinacache',
                'verycdn'
                'webcache',
                'x-cacheable',
                'x-fastly',
                'yunjiasu',
            ]),
            'cname': {
                'tbcache.com':u'taobao', # 应该是淘宝自己的。。。。
                'tcdn.qq.com':u'tcdn.qq.com', # 应该是腾讯的。。。
                'yunjiasu-cdn':u'Baiduyun', # 百度云加速
                'kunlunar.com':u'ALiyun', # 阿里云
                'kunlunca.com':u'ALiyun', # 阿里云
                'kxcdn.com':u'KeyCDN', # KeyCDN
                'lswcdn.net':u'Leaseweb', # Leaseweb
                'lxcdn.com':u'ChinaCache', # 网宿科技
                'lxdns.com':u'ChinaCache', # 网宿科技
                # 其余的特征可以自己找一下
            }
        }
