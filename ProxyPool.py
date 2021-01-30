import os
import requests
import Settings
import random


def get_proxy():
    while True:
        files = list(filter(lambda f: "|" not in f, os.listdir(Settings.POOL_DIR)))
        if not files:
            return None
        ip_port = random.choice(files)
        # files.sort(key=lambda f: os.path.getmtime(os.path.join(Settings.POOL_DIR, f)))
        if check(ip_port):
            break
    return ip_port

def check(ip_port):
    proxies = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    try:
        requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
        return True
    except Exception:
        return False