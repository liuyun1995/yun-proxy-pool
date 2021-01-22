import threading


class JiangXianLi(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.site_name = "快代理"

    def run(self):
        print(self.site_name + "-> 测试")