import queue
import re
import time
import bloompy
import requests
import Utils
import threading
import random


class KuaiDaiLi(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.site_name = "快代理"
        self.init_urls = ["/free/inha/1/"]
        self.url_prefix = "https://www.kuaidaili.com"
        self.header = {
            "Host": "www.kuaidaili.com",
            "Referer": "https://www.kuaidaili.com/free/",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }
        self.url_queue = queue.Queue(100)
        self.bloom_filter = bloompy.BloomFilter(error_rate=0.001, element_num=10 ** 3)

    def run(self):
        for url in self.init_urls:
            self.bloom_filter.add(url)
            self.url_queue.put(self.url_prefix + url, block=True, timeout=5)
        is_continue = True
        while is_continue:
            is_continue = self.__do_crawl()
            time.sleep(random.randint(1, 5))

    def __do_crawl(self):
        url = self.url_queue.get(block=True, timeout=5)
        if url is None:
            return False
        response = requests.get(url, headers=self.header)
        self.__parse_url(response.text)
        self.__parse_data(response.text)
        return True

    def __parse_url(self, html):
        nav_div = re.search(r"<div id=\"listnav\">(.*?)</div>", html, re.M | re.I | re.S)
        if nav_div is None:
            return
        url_list = re.findall(r"<a href=\"(.*?)\".*?>.*?</a>", nav_div.group(1), re.M | re.I | re.S)
        if url_list is None:
            return
        for url in url_list:
            if self.bloom_filter.exists(url):
                continue
            self.bloom_filter.add(url)
            self.url_queue.put(self.url_prefix + url, block=True, timeout=5)

    def __parse_data(self, html):
        lines = re.findall(r"<tr>(.*?)</tr>", html, re.M | re.I | re.S)
        if lines is None:
            return
        for line in lines:
            ip = re.search(r"<td data-title=\"IP\">(.*?)</td>", line, re.S)
            port = re.search(r"<td data-title=\"PORT\">(.*?)</td>", line, re.S)
            if ip is None or port is None:
                continue
            msg = Utils.check_and_save1(ip.group(1), port.group(1))
            print(self.site_name + "->" + msg)