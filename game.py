from constants import *
import random


# helpers
def is_collision(x1, y1, x2, y2):  # can pass snake 2 here, or do it on server side
    return x1 == x2 and y1 == y2


# game objects
class Resource:
    def __init__(self):
        self.x = random.randint(10, int(BOARD_SIZE[0] / BLOCK_SIZE) - 11) * BLOCK_SIZE
        self.y = random.randint(8, int(BOARD_SIZE[1] / BLOCK_SIZE) - 9) * BLOCK_SIZE

    def move(self):
        tmp_x = random.randint(0, int(BOARD_SIZE[0] / BLOCK_SIZE) - 1) * BLOCK_SIZE
        tmp_y = random.randint(0, int(BOARD_SIZE[1] / BLOCK_SIZE) - 1) * BLOCK_SIZE

        while self.x == tmp_x and self.y == tmp_y:
            tmp_x = random.randint(0, int(BOARD_SIZE[0] / BLOCK_SIZE) - 1) * BLOCK_SIZE
            tmp_y = random.randint(0, int(BOARD_SIZE[1] / BLOCK_SIZE) - 1) * BLOCK_SIZE

        self.x = tmp_x
        self.y = tmp_y


class Snake:
    def __init__(self, player_num):
        self.length = 1
        if player_num == 1:
            self.x = [3 * BLOCK_SIZE]
            self.y = [3 * BLOCK_SIZE]
            self.direction = 'right'
            self.next_direction = 'right'
        elif player_num == 2:
            self.x = [(int(BOARD_SIZE[0] / BLOCK_SIZE) - 4) * BLOCK_SIZE]
            self.y = [(int(BOARD_SIZE[1] / BLOCK_SIZE) - 4) * BLOCK_SIZE]
            self.direction = 'left'
            self.next_direction = 'left'

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
        # update body, iterating from the back of the snake
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

    def increase_length(self):
        self.length += 1
        self.x.append(0)  # give it any value, will update next iteration
        self.y.append(0)  # give it any value, will update next iteration


class Game:
    def __init__(self):
        self.p1 = Snake(1)
        self.p2 = Snake(2)
        self.p1_reset = False
        self.p2_reset = False
        self.resource = Resource()
        self.ready = False
        self.scores = [0, 0]
        self.over = False

    def reset(self):
        self.p1 = Snake(1)
        self.p2 = Snake(2)
        self.p1_reset = False
        self.p2_reset = False
        self.resource = Resource()
        self.scores = [0, 0]
        self.over = False

    def handle_key_event(self, player_num, key):
        if player_num == 1:
            if key == 'u':
                self.p1.set_dir_up()
            elif key == 'd':
                self.p1.set_dir_down()
            elif key == 'l':
                self.p1.set_dir_left()
            elif key == 'r':
                self.p1.set_dir_right()
            elif key == 'reset' and self.over:
                self.p1_reset = True
        elif player_num == 2:
            if key == 'u':
                self.p2.set_dir_up()
            elif key == 'd':
                self.p2.set_dir_down()
            elif key == 'l':
                self.p2.set_dir_left()
            elif key == 'r':
                self.p2.set_dir_right()
            elif key == 'reset' and self.over:
                self.p2_reset = True
        else:
            raise "Invalid player number"

    def update(self):
        if self.p1_reset and self.p2_reset:
            self.reset()

        elif not self.over:
            self.p1.move()  # moves snake and draws it

            # snake eating resource
            if is_collision(self.p1.x[0], self.p1.y[0], self.resource.x, self.resource.y):
                self.p1.increase_length()
                self.resource.move()
                self.scores[0] += 1
            
            if is_collision(self.p2.x[0], self.p2.y[0], self.resource.x, self.resource.y):
                self.p2.increase_length()
                self.resource.move()
                self.scores[1] += 1

            # snake collide head to head
            self.over = is_collision(self.p1.x[0], self.p1.y[0], self.p2.x[0], self.p2.y[0])
            if self.over:
                return

            # snake colliding with itself or the body of the other snake
            for i in range(2, self.p1.length):
                self.over = is_collision(self.p1.x[0], self.p1.y[0], self.p1.x[i], self.p1.y[i]) or is_collision(self.p2.x[0], self.p2.y[0], self.p1.x[i], self.p1.y[i])
                if self.over:
                    return
            
            for i in range(2, self.p2.length): 
                self.over = is_collision(self.p2.x[0], self.p2.y[0], self.p2.x[i], self.p2.y[i]) or is_collision(self.p1.x[0], self.p1.y[0], self.p2.x[i], self.p2.y[i])
                if self.over:
                    return
            
            self.p2.move()  # moves second snake and draws it
