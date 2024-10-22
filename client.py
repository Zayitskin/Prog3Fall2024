import socket

ADDR = "127.0.0.1"
PORT = 1234

def server_connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ADDR, PORT))
        print(f"Server found. Connecting to {ADDR}:{PORT}")
        send = b""
        while send != b"close":
            recv = sock.recv(1024).decode(encoding="UTF-8")
            recv = recv.split("|")
            if len(recv) == 2:
                data, command = recv[0], recv[1]
            elif len(recv) == 1:
                data = recv[0]
                command = "send"
            if command == "send":
                send = bytes(input("Input: "), encoding="UTF-8")
                sock.send(send)

if __name__ == "__main__":
    server_connect()
