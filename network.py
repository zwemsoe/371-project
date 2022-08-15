import pickle
import socket
from constants import *

# client socket handler
class Network:
    def __init__(self):
        # open tcp socket on client
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('localhost', SERVER_PORT)
        self.id = self.connect()
        print(f"you are player {self.id}")

    def connect(self):
        try:
            self.server.connect(self.addr)	
            return self.server.recv(2048).decode()
        except Exception as e:
            print(str(e))

    def send(self, data):
        try:
            self.server.send(str.encode(data))
            return pickle.loads(self.server.recv(4096))
        except socket.error as e:
            return str(e)
