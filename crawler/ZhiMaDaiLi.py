import requests
import re
import Utils
import time
import threading
import random
import Settings

class ZhiMaDaiLi((threading.Thread)):

    def __init__(self):
        threading.Thread.__init__(self)
        self.site_name = "芝麻代理"
        self.url = "http://wapi.http.linkudp.com/index/index/get_free_ip"
        self.header = {
            "Host": "wapi.http.linkudp.com",
            "Referer": "http://h.zhimaruanjian.com/",
            "Connection": "keep-alive",
            "Accept": "text/html, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }

    def run(self):
        page = 1
        total_page = 1
        while page <= total_page:
            proxy_num = Utils.get_proxy_num()
            if proxy_num >= Settings.POOL_MAX_NUM:
                time.sleep(random.randint(5, 10))
                continue
            data = {"page": page}
            response = requests.post(self.url, headers=self.header, data=data)
            json = response.json()
            if json['code'] != '1':
                continue
            ret_data = json['ret_data']
            total_page = ret_data['last']
            self.__parse_data(ret_data['html'])
            page += 1
            time.sleep(random.randint(1, 5))

    def __parse_data(self, html):
        lines = re.findall(r"<tr class=\"tr\">(.*?)</tr>", html, re.M | re.I | re.S)
        if lines is None:
            return
        for line in lines:
            try:
                columns = re.findall(r"<td>(.*?)</td>", line, re.S)
                ip = re.search(r"(\d{1,3}\.){3}\d{1,3}", columns[0], re.M | re.I | re.S).group(0)
                port = columns[1]
                ip_port, message = Utils.check_and_save1(ip, port)
                print("{:>8s} {:>12s} {:s}".format("[" + self.site_name + "]", ip_port, message))
            except Exception:
                continue