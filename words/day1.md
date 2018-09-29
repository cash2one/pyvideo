# Python 多线程
## threading模块
Simple Example:
```
impirt threading
t1 = threading.Thread(target=func, args=(parameter,))  # 创建线程
t1.setDaemon(True)  # 声明为守护线程，必须在start()方法调用之前设置,如果不设置为守护线程，子线程会不限挂起。设置为守护线程，当子线程启动后，父线程也继续执行，当父线程执行完后，没有等待子线程，父线程退出了，同时子线程也一同结束
t1.start()  # 开始线程活动
t1.join # 等待线程终止 在子线程完成运行之前，这个子线程的父线程将一直被阻塞

```
Class Example:
```
import threading
class MyThread(threading.Thread):
    def __init__(self, args):
        super(MyThread, self).__init__() # 重构run函数必须要写
        self.args = args

    def run(self):
        print('run')
```

