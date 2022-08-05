import socket
from _thread import *

def client_thread(conn):
    print("starting client thread")

def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('localhost', 8000))
    except socket.error as e:
        print(str(e))

    s.listen(2)
    print("listening on 8000")   
    while True:
        conn, addr = s.accept()
        print("connected to: ", addr)
        start_new_thread(client_thread, (conn,))


run_server()