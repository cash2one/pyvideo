import threading
import time

class MyThread(threading.Thread):
    def __init__(self, runback):
        super().__init__()
        self.runback = runback

        self.setDaemon(True)

    def run(self):
        self.runback()
        print('ddddd:'+ threading.currentThread().getName() + '\n')
        print(threading.activeCount())