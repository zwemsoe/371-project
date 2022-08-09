import socket
import pygame
from pygame.locals import *
import time
import random
from constants import *

class Network:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('localhost', SERVER_PORT)
        self.id = self.connect()
        print(f"You are player {self.id}")

    def connect(self):
        try:
            self.server.connect(self.addr)	
            return self.server.recv(2048).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.server.send(str.encode(data))
            reply = self.server.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)



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
    def __init__(self, surface):
        self.parent_screen = surface  # take in and store the screen to be able to refresh it later
        self.image_head = pygame.image.load("resources/greenhead.png").convert()  # load head image
        self.image_body = pygame.image.load("resources/greenblock.png").convert()  # load body image
        self.direction = 'right'
        self.next_direction = 'right'

        self.length = 1
        self.x = [BLOCK_SIZE]  # starting x loc
        self.y = [BLOCK_SIZE]  # starting y loc

    def set_dir_up(self):
        if self.direction != 'down':
            self.next_direction = 'up'

    def set_dir_down(self):
        if self.direction != 'up':
            self.next_direction = 'down'

    def set_dir_left(self):
        if self.direction != 'right':
            self.next_direction = 'left'

    def set_dir_right(self):
        if self.direction != 'left':
            self.next_direction = 'right'

    def move(self):
        # update body
        for i in range(self.length - 1, 0, -1):  # iterate from the back of the snake
            self.x[i] = self.x[i - 1]  # set snake x position to the 1 position closer to the head
            self.y[i] = self.y[i - 1]  # set snake y position to the 1 position closer to the head

        self.direction = self.next_direction
        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
            if self.y[0] < 0:
                self.y[0] += BOARD_SIZE[1]
        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE
            if self.y[0] >= BOARD_SIZE[1]:
                self.y[0] -= BOARD_SIZE[1]
        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
            if self.x[0] < 0:
                self.x[0] += BOARD_SIZE[0]
        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE
            if self.x[0] >= BOARD_SIZE[0]:
                self.x[0] -= BOARD_SIZE[0]

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(0)  # give it any value, will update next iteration
        self.y.append(0)  # give it any value, will update next iteration

    def draw(self):
        self.parent_screen.blit(self.image_head, (self.x[0], self.y[0]))  # draw snake head
        for i in range(1, self.length):
            self.parent_screen.blit(self.image_body, (self.x[i], self.y[i]))  # draw each body blocks



class Game:
    def __init__(self):
        pygame.init()
        self.network = Network()
        self.surface = pygame.display.set_mode(BOARD_SIZE)  # create screen with size x, y
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.resource = Resource(self.surface)
        self.resource.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.resource = Resource(self.surface)
    
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, FONT_COLOR)
        self.surface.blit(score, (BOARD_SIZE[0] - 150, 10))

    def show_game_over(self):
        self.surface.fill(BOARD_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, FONT_COLOR)
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, FONT_COLOR)
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
    
    def update(self):
        self.surface.fill(BOARD_COLOR)  # fill screen with color
        self.snake.move()  # moves snake and draws it
        self.resource.draw()  # draw resource
        self.display_score()
        pygame.display.flip()  # redraw/refresh UI window here

        # snake eating resource
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.resource.x, self.resource.y):
            self.snake.increase_length()
            self.resource.move()

        # snake colliding with itself
        for i in range(4, self.snake.length):  # can't collide with itself until at least the 5th element (idx: 4)
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred!"
    
    def run(self):
        running = True
        ready = False

        while running:
            msg = self.network.send('get_updates')
            print(msg)
            for event in pygame.event.get():
                if event.type == QUIT:  # exit if close button pressed
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # exit if esc button pressed
                        running = False
                    if event.key == K_RETURN:
                        # pause = not pause  # can pause the game, disable for multiplayer
                        ready = True
                    if ready:
                        if event.key == K_UP:
                            self.snake.set_dir_up()
                        if event.key == K_DOWN:
                            self.snake.set_dir_down()
                        if event.key == K_LEFT:
                            self.snake.set_dir_left()
                        if event.key == K_RIGHT:
                            self.snake.set_dir_right()
            try:
                self.update()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(1)  # wait between updates
    
    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

if __name__ == '__main__':
    game = Game()
    game.run()
