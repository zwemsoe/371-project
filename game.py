import pygame
from pygame.locals import *
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

def draw_block():
    surface.fill((255, 176, 227))
    surface.blit(block, (block_x, block_y))
    pygame.display.flip()

# game logic
# probably need Grid, Snake, Apple, and some other classes
# run game
if __name__ == '__main__':
    pygame.init()

    surface = pygame.display.set_mode((800, 800))
    surface.fill((255, 176, 227))

    block = pygame.image.load("resources/block.jpg").convert()
    block_x, block_y = 0, 0

    surface.blit(block, (block_x, block_y))
    pygame.display.flip() # refresh UI window

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_UP:
                    block_y -= 40
                    draw_block()
                if event.key == K_DOWN:
                    block_y += 40
                    draw_block()
                if event.key == K_LEFT:
                    block_x -= 40
                    draw_block()
                if event.key == K_RIGHT:
                    block_x += 40
                    draw_block()

