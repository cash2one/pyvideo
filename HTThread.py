import threading

class HTThread(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def run(self):
        self.callback()
