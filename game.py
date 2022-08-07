import socket
import pygame
from pygame.locals import *
import time
import random

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
# probably need Grid, Snake, Resource, and some other classes
# run game

BLOCK_SIZE = 40
BOARD_SIZE = (800, 800)
BOARD_COLOR = (155, 155, 155)

class Resource:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/diamond.png").convert_alpha()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, int(BOARD_SIZE[0] / BLOCK_SIZE)) * BLOCK_SIZE
        self.y = random.randint(1, int(BOARD_SIZE[1] / BLOCK_SIZE)) * BLOCK_SIZE

class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface  # take in and store the screen to be able to refresh it later
        self.image = pygame.image.load("resources/greenblock.png").convert()  # load block image into named variable
        self.direction = 'right'

        self.length = length
        self.x = [BLOCK_SIZE] * length  # starting x
        self.y = [BLOCK_SIZE] * length  # starting y

    def set_dir_up(self):
        self.direction = 'up'

    def set_dir_down(self):
        self.direction = 'down'

    def set_dir_left(self):
        self.direction = 'left'

    def set_dir_right(self):
        self.direction = 'right'

    def move(self):
        # update body
        for i in range(self.length - 1, 0, -1):  # iterate from the back of the snake
            self.x[i] = self.x[i - 1]  # set snake x position to the 1 position closer to the head
            self.y[i] = self.y[i - 1]  # set snake y position to the 1 position closer to the head

        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE
        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))  # draw each snake block on screen


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(BOARD_SIZE)  # create screen with size x, y
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.resource = Resource(self.surface)
        self.resource.draw()
        self.running = True

    def update(self):
        self.surface.fill(BOARD_COLOR)  # fill screen with color
        self.snake.move()  # moves snake and draws it
        self.resource.draw()  # draw resource
        pygame.display.flip()  # redraw/refresh UI window here

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:  # exit if close button pressed
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # exit if esc button pressed
                        self.running = False
                    if event.key == K_UP:
                        self.snake.set_dir_up()
                    if event.key == K_DOWN:
                        self.snake.set_dir_down()
                    if event.key == K_LEFT:
                        self.snake.set_dir_left()
                    if event.key == K_RIGHT:
                        self.snake.set_dir_right()
            self.update()
            time.sleep(.5)  # wait half a second between updates


if __name__ == '__main__':
    game = Game()
    game.run()