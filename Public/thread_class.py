import threading
import time

class MyThread(threading.Thread):
    def __init__(self, target, args=None):
        super().__init__()
        self.target = target
        self.args = args

        self.setDaemon(True)

    def run(self):
        self.target(self.args)
        print('currentThread:'+ threading.currentThread().getName() + '\n')
        print(threading.activeCount())