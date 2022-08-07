import pygame
from pygame.locals import *
import time
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
class Snake:
    def __init__(self, surface):
        self.parent_screen = surface # take in and store the screen to be able to refresh it later
        self.block = pygame.image.load("resources/block.jpg").convert() # load block image into named variable
        self.x = 40 # starting x
        self.y = 40 # starting y
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        if self.direction == 'up':
            self.y -= 40
        if self.direction == 'down':
            self.y += 40
        if self.direction == 'left':
            self.x -= 40
        if self.direction == 'right':
            self.x += 40
        self.draw()

    def draw(self):
        self.parent_screen.fill((255, 176, 227)) # fill screen with color
        self.parent_screen.blit(self.block, (self.x, self.y)) # draw block on screen
        pygame.display.flip() # redraw/refresh UI window


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800)) # create screen with size x, y
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
            self.snake.walk()
            time.sleep(.5)


if __name__ == '__main__':
    game = Game()
    game.run()