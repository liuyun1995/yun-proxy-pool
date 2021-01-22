import queue
import re
import time
import bloompy
import requests
import Utils
import threading
import random


class XiLaDaiLi(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.site_name = "西拉代理"
        self.init_urls = ["/gaoni/1/"]
        self.url_prefix = "http://www.xiladaili.com"
        self.header = {
            "Host": "www.xiladaili.com",
            "Referer": "http://www.xiladaili.com/gaoni/",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }
        self.url_queue = queue.PriorityQueue(100)
        self.bloom_filter = bloompy.BloomFilter(error_rate=0.001, element_num=10 ** 3)

    def run(self):
        for url in self.init_urls:
            full_url = self.url_prefix + url
            self.bloom_filter.add(url)
            self.url_queue.put([int(re.search("([0-9]+)", full_url).group(1)), full_url], timeout=5)
        is_continue = True
        while is_continue:
            is_continue = self.__do_crawl()
            time.sleep(random.randint(1, 5))

    def __do_crawl(self):
        url = self.url_queue.get(block=True, timeout=5)
        if url is None:
            return False
        response = requests.get(url[1], headers=self.header)
        self.__parse_url(response.text)
        self.__parse_data(response.text)
        return True

    def __parse_url(self, html):
        nav_div = re.search(r"<ul class=\"pagination justify-content-center\">(.*?)</ul>", html, re.M | re.I | re.S)
        if nav_div is None:
            return
        url_list = re.findall(r"<a .*?href=\"(.*?)\".*?>.*?</a>", nav_div.group(1), re.M | re.I | re.S)
        if url_list is None:
            return
        for url in url_list:
            if url in ["/gaoni", "/gaoni/", "/gaoni/0", "/gaoni/0/", "/gaoni/1", "/gaoni/1/"]:
                continue
            if self.bloom_filter.exists(url):
                continue
            full_url = self.url_prefix + url
            self.bloom_filter.add(url)
            self.url_queue.put([int(re.search("([0-9]+)", full_url).group(1)), full_url], timeout=5)

    def __parse_data(self, html):
        table = re.search(r"<table class=\"fl-table\">(.*?)</table>", html, re.M | re.I | re.S).group(1)
        tbody = re.search(r"<tbody>(.*?)</tbody>", table, re.M | re.I | re.S).group(1)
        lines = re.findall(r"<tr>(.*?)</tr>", tbody, re.M | re.I | re.S)
        if lines is None:
            return
        for line in lines:
            ip_port = re.findall(r"<td>(.*?)</td>", line, re.M | re.I | re.S)[0]
            if ip_port is None:
                continue
            msg = Utils.check_and_save2(ip_port)
            print(self.site_name + "->" + msg)