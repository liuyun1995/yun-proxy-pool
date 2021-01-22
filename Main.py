from crawler.PoolFlusher import PoolFlusher
from crawler.JiangXianLi import JiangXianLi
from crawler.KuaiDaiLi import KuaiDaiLi
from crawler.XiLaDaiLi import XiLaDaiLi
from crawler.ZhiMaDaiLi import ZhiMaDaiLi

t0 = PoolFlusher()
t1 = KuaiDaiLi()
t2 = ZhiMaDaiLi()
t3 = XiLaDaiLi()
t4 = JiangXianLi()

t0.setDaemon(True)
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
t4.setDaemon(True)

print("======== Start ========")

t0.start()
t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print("======== Done! ========")
