from __future__ import print_function
from app.App import App as real_app
import zerorpc
import threading
import time

class RealAppIniter():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.real_app = None
        self.thread = threading.Thread(target = self.run)
        self.start_backend_client()
        print('RealAppIniter inited!')
        time.sleep(0.1)

    def start_backend_client(self):
        self.thread.setDaemon(True)
        self.thread.start()

    def run(self):
        client = zerorpc.Client()
        client.connect("tcp://" + self.ip + ":" + self.port)
        self.real_app = real_app(client)
        self.real_app.run()    

    def get_real_app(self):
        print('get_real_app', 'was called')
        return self.real_app