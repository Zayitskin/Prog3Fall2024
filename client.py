import socket
import os

from games import print_ttt
from server import clients

ADDR = "127.0.0.1"
PORT = 1235

def server_connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ADDR, PORT))
        print(f"Server found. Connecting to {ADDR}:{PORT}")
        send = b""

        while True:
                send = bytes(input("Enter your username: "), encoding="UTF-8")
                if send:
                    confirm = input(f"Your username is {send.decode(encoding='UTF-8')}? Y/N ").lower()
                    if confirm == "yes" or confirm == "y":
                        sock.send(send)
                        break
                print("Enter something. Anything at all. Please. I crave inputs.")

        while send != b"close":
            recv = sock.recv(1024).decode(encoding="UTF-8")
            recv = recv.split("|")
            if len(recv) == 2:
                data, command = recv[0], recv[1]
            elif len(recv) == 1:
                data = recv[0]
                command = "send"
            if command == "clear":
                os.system("clear")
            print(data)
            if command == "send":
                while True:
                    send = bytes(input("Input: "), encoding="UTF-8")
                    if send:
                        sock.send(send)
                        break
                    print("Enter something. Anything at all. Please. I crave inputs.")
            elif command == "print ttt":
                print_ttt(data)

if __name__ == "__main__":
    server_connect()
