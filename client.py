import pygame
import time
from pygame.locals import *
from constants import *
from network import *

pygame.font.init()
window = pygame.display.set_mode(BOARD_SIZE)
pygame.display.set_caption("Multiplayer Snake Game")


def get_result_message(game, player_id):
    if game.scores[0] == game.scores[1]:
        return f"It's a tie! You both scored {game.scores[0]} points!"
    winner = 1 if game.scores[0] > game.scores[1] else 2
    if player_id == winner:
        return f"You win! Your score is {game.scores[player_id-1]} points!"
    return f"You lose! Your score is {game.scores[player_id-1]} points!"


def display_info(game, player_id):
    font = pygame.font.SysFont(FONT_STYLE, 30)
    player_color = "Green" if player_id == 1 else "Blue"
    color = font.render(f"You are {player_color}", True, FONT_COLOR)
    score = font.render(f"Score: {game.scores[player_id-1]}", True, FONT_COLOR)
    window.blit(color, (30, 10))
    window.blit(score, (BOARD_SIZE[0] - 150, 10))


def show_over(result_message):
    font = pygame.font.SysFont(FONT_STYLE, 30)
    line1 = font.render("Game is over", True, FONT_COLOR)
    window.blit(line1, (200, 300))
    line2 = font.render(f"{result_message}", True, FONT_COLOR)
    window.blit(line2, (200, 350))
    line3 = font.render("Press \"r\" to restart", True, FONT_COLOR)
    window.blit(line3, (200, 400))
    pygame.display.flip()


def display_snakes(game):
    heads = [pygame.image.load("resources/greenhead.png").convert(),
             pygame.image.load("resources/bluehead.png").convert()]  # load head images
    bodies = [pygame.image.load("resources/greenblock.png").convert(),
              pygame.image.load("resources/blueblock.png").convert()]  # load body images
    window.blit(heads[0], (game.p1.x[0], game.p1.y[0]))
    window.blit(heads[1], (game.p2.x[0], game.p2.y[0]))
    for i in range(1, game.p1.length):
        window.blit(bodies[0], (game.p1.x[i], game.p1.y[i]))
    for i in range(1, game.p2.length):
        window.blit(bodies[1], (game.p2.x[i], game.p2.y[i]))


def display_resource(game):
    image = pygame.image.load("resources/diamond.png").convert_alpha()
    window.blit(image, (game.resource.x, game.resource.y))


def draw_grid_lines():
    for x in range(0, BOARD_SIZE[0], BLOCK_SIZE):
        pygame.draw.line(window, LINE_COLOR, (x, 0), (x, BOARD_SIZE[1]))
    for y in range(0, BOARD_SIZE[1], BLOCK_SIZE):
        pygame.draw.line(window, LINE_COLOR, (0, y), (BOARD_SIZE[0], y))

def display_game(game, player_id):
    window.fill(BOARD_COLOR)
    if not game.ready:
        font = pygame.font.SysFont(FONT_STYLE, 30)
        text = font.render(f"You are player {player_id}. Waiting for another player...", 1, (255, 0, 0))
        window.blit(text, (BOARD_SIZE[0]/2 - text.get_width()/2, BOARD_SIZE[1]/2 - text.get_height()/2))
    else:
        draw_grid_lines()
        display_snakes(game)
        display_resource(game)
        display_info(game, player_id)

    pygame.display.update()


def game_loop():
    over = False
    clock = pygame.time.Clock()
    net = Network()
    player_id = int(net.id)
    result_message = 'Other player has disconnected.'
    speed = 0.4
    one_shot = False

    while not over:
        clock.tick(60)
        try:
            game = net.send("game_state")
        except Exception as e:
            over = True
            print("client: something went wrong")
            print(str(e))
            break

        if game.over and not one_shot:
            display_game(game, player_id)
            result_message = get_result_message(game, player_id)
            show_over(result_message)
            one_shot = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                net.send('quit')
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    net.send('u')
                if event.key == K_DOWN:
                    net.send('d')
                if event.key == K_LEFT:
                    net.send('l')
                if event.key == K_RIGHT:
                    net.send('r')
                if event.key == K_RIGHT:
                    net.send('r')
                if event.key == K_r:
                    net.send('reset')

        if not game.over:
            one_shot = False
            display_game(game, player_id)

        time.sleep(speed)


def welcome_screen():
    start = False

    while not start:
        window.fill(BOARD_COLOR)
        font = pygame.font.SysFont(FONT_STYLE, 60)
        text = font.render("Press enter to play!", 1, (255, 0, 0))
        window.blit(text, (BOARD_SIZE[0]/2 - text.get_width()/2, BOARD_SIZE[1]/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    start = True
    game_loop()


if __name__ == '__main__':
    welcome_screen()
