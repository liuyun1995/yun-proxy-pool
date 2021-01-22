import os
import requests
import Settings


def check_and_save1(ip, port):
    status, message = _check(ip, port)
    if status:
        _save(ip, port)
    return message


def check_and_save2(ip_port):
    if ip_port is None:
        return
    return check_and_save1(ip_port.split(":")[0], ip_port.split(":")[1])


def _check(ip, port):
    if ip is None or port is None:
        return False
    ip_port = ip + ":" + port
    proxies = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    try:
        requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
        return True, "\033[32m[测试成功]\033[0m" + ip_port
    except Exception:
        return False, "\033[31m[测试失败]\033[0m" + ip_port


def _save(ip, port):
    ip_port = ip + ":" + port
    if not os.path.exists(Settings.POOL_DIR):
        os.mkdir(Settings.POOL_DIR)
    proxy_num = get_proxy_num()
    is_exist = os.path.exists(Settings.POOL_DIR + Settings.DELIMITER + ip_port)
    if proxy_num < Settings.POOL_MAX_NUM and not is_exist:
        os.mknod(Settings.POOL_DIR + Settings.DELIMITER + ip_port)


def get_proxy_num():
    num = 0
    for file in os.listdir(Settings.POOL_DIR):
        if os.path.isfile(os.path.join(Settings.POOL_DIR, file)):
            num = num + 1
    return num