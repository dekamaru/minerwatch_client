import queue
import logging


class ThreadNetwork:
    def __init__(self):
        self.clients = {}

    def connect(self, name):
        if name not in self.clients.keys():
            self.clients[name] = queue.Queue()

    def send_message(self, to, message, wait_done=False):
        if to not in self.clients.keys():
            logging.error('Client ' + to + ' not found in ThreadNetwork')
        else:
            self.clients[to].put(message)
            if wait_done:
                self.clients[to].join()  # lock while receiver do his job

    def receive_message(self, receiver, immediate_done=True):
        item = self.clients[receiver].get()
        if immediate_done:
            self.done_message(receiver)
        return item

    def done_message(self, receiver):
        self.clients[receiver].task_done()