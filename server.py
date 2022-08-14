import socket
from _thread import *
from game import *
from constants import *
import pickle


player_count = 0
game = None
players = {}

def client_thread(conn, player):
    global player_count
    global game
    global players
    print(f"starting player-{player} thread")
    # send back player id
    conn.send(str.encode(str(player)))
    while True:
        try:
            data = conn.recv(4096).decode()
            print(f"received from {player}: {data}")
            if game.ready:
                if data != "game_state":
                    if data == 'quit':
                        game.ready = False
                        conn.sendall(pickle.dumps(game))
                        break
                    game.handle_key_event(player, data)
                game.update()  
            conn.sendall(pickle.dumps(game))
                    
        except Exception as e:
            print("server: something went wrong")
            print(str(e))
            break
    
    player_count -= 1
    del players[player]
    # if 1 player left, start new game
    game = None if player_count == 0 else Game()
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(('localhost', SERVER_PORT))
except socket.error as e:
    print(str(e))

s.listen(2)
print(f"listening on {SERVER_PORT}")  
 
while True:
    conn, addr = s.accept()
    print("connected to: ", addr)
    player_count += 1
    
    # picking player id
    player = 1
    if 1 in players:
        player = 2
        players[2] = 1
    else:
        players[1] = 1

    if player_count < 2:
        game = Game() if game is None else game
        print("creating a new game...")
    else:
        game.ready = True
        print("both players ready")
    start_new_thread(client_thread, (conn,player))
