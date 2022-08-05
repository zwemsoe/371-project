import pygame
import socket

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('localhost', 8000)

    def connect(self):
        try:
            self.client.connect(self.addr)	
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)

# game logic
# probably need Grid, Snake, Apple, and some other classes
# run game