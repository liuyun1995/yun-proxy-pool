import threading
import requests
import Utils
import Settings
import time
import random


class JiangXianLi(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.site_name = "JiangXianLi"
        self.init_url = "https://ip.jiangxianli.com/api/proxy_ips"
        self.header = {
            "Host": "ip.jiangxianli.com",
            "Referer": "https://github.com/jiangxianli/ProxyIpLib",
            "Connection": "keep-alive",
            "Accept": "text/html, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }

    def run(self):
        page = 1
        last_page = 1
        while page <= last_page:
            param = {
                "page": page,
                "country": "中国",
            }
            proxy_num = Utils.get_proxy_num()
            if proxy_num >= Settings.POOL_MAX_NUM:
                time.sleep(random.randint(5, 10))
                continue
            response = requests.get(url=self.init_url, headers=self.header, params=param)
            json = response.json()["data"]
            last_page = json["last_page"]
            data = json["data"]
            for item in data:
                ip = item["ip"]
                port = item["port"]
                ip_port, message = Utils.check_and_save1(ip, port)
                print("{:>8s} {:>12s} {:s}".format("[" + self.site_name + "]", ip_port, message))
            page += 1
            time.sleep(2)

