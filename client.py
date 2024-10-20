
import asyncio
import socket

from sock_coro import co_recv
from sock_coro import co_send

ADDR = "127.0.0.1"
PORT = 1234

def server_connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ADDR, PORT))
        send = b""
        while send != b"close":
            recv = sock.recv(1024)
            print(recv.decode(encoding="UTF-8"))
            send = bytes(input("Input: "), encoding="UTF-8")
            sock.send(send)

if __name__ == "__main__":
    server_connect()
