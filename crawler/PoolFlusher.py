import os
import threading
import time
import requests
import Settings


class PoolFlusher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        is_run = True
        round = 0
        while is_run:
            round += 1
            is_run = self.flash_proxy(round)
            time.sleep(3)

    def flash_proxy(self, round):
        file_list = os.listdir(Settings.POOL_DIR)
        if file_list is None:
            return False
        for old_file in file_list:
            if "|" in old_file:
                ip_port = old_file.split("|")[0]
                fail_num = old_file.split("|")[1]
            else:
                ip_port = old_file
                fail_num = None
            new_file = None
            proxies = {"http": "http://" + ip_port, "https": "https://" + ip_port}
            try:
                requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
                new_file = ip_port
            except Exception:
                if fail_num:
                    fail_num = int(fail_num) + 1
                else:
                    fail_num = 1
                if fail_num <= 3:
                    new_file = ip_port + "|" + str(fail_num)
            os.remove(os.path.join(Settings.POOL_DIR, old_file))
            try:
                if new_file:
                    os.mknod(os.path.join(Settings.POOL_DIR, new_file))
            except Exception:
                continue
        print("========== 第%s轮：IP代理池校验完毕! =========="%(round))
        return True