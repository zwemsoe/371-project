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
BOARD_SIZE = (1000, 800)
BOARD_COLOR = (155, 155, 155)
FONT_COLOR = (255, 255, 255)


class Resource:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/diamond.png").convert_alpha()
        self.x = random.randint(10, int(BOARD_SIZE[0] / BLOCK_SIZE) - 11) * BLOCK_SIZE
        self.y = random.randint(8, int(BOARD_SIZE[1] / BLOCK_SIZE) - 9) * BLOCK_SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        tmp_x = random.randint(0, int(BOARD_SIZE[0] / BLOCK_SIZE) - 1) * BLOCK_SIZE
        tmp_y = random.randint(0, int(BOARD_SIZE[1] / BLOCK_SIZE) - 1) * BLOCK_SIZE

        while self.x == tmp_x and self.y == tmp_y:
            tmp_x = random.randint(0, int(BOARD_SIZE[0] / BLOCK_SIZE) - 1) * BLOCK_SIZE
            tmp_y = random.randint(0, int(BOARD_SIZE[1] / BLOCK_SIZE) - 1) * BLOCK_SIZE

        self.x = tmp_x
        self.y = tmp_y


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

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))  # draw each snake block on screen


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(BOARD_SIZE)  # create screen with size x, y
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.resource = Resource(self.surface)
        self.resource.draw()
        self.running = False

    def is_collision(self, s_x, s_y, r_x, r_y):  # can pass snake 2 here, or do it on server side
        if s_x == r_x:
            if s_y == r_y:
                return True
        return False

    def update(self):
        self.surface.fill(BOARD_COLOR)  # fill screen with color
        self.snake.move()  # moves snake and draws it
        self.resource.draw()  # draw resource
        self.display_score()
        pygame.display.flip()  # redraw/refresh UI window here

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.resource.x, self.resource.y):
            self.snake.increase_length()
            self.resource.move()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, FONT_COLOR)
        self.surface.blit(score, (BOARD_SIZE[0] - 150, 10))

    def run(self):
        self.running = True
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
            time.sleep(.2)  # wait half a second between updates


if __name__ == '__main__':
    game = Game()
    game.run()
