import socket
from _thread import *
from game import *
from constants import *
import pickle


playerCount = 0
game = {}

def client_thread(conn, player):
    print("starting client thread")
    conn.send(str.encode(str(player)))
    while True:
        try:
            data = conn.recv(4096).decode()
            # if game.ready:
            #     if data == "key_event":
            #         game.handle_key_event(player, data)
            #     game.update(player)  
            
            conn.sendall(pickle.dumps(game))
                    
        except:
            break
    
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
    playerCount += 1
    player = 0
    if playerCount < 2:
        game = Game()
        print("Creating a new game...")
    else:
        game.ready = True
        player = 1
        print("ready")
    start_new_thread(client_thread, (conn,player))
