import random
import asyncio
import socket

from games import rps
from games import ttt
from games import connect

from sock_coro import co_accept
from sock_coro import co_recv
from sock_coro import co_send

ADDR = "127.0.0.1"
PORT = 1234

async def server_select(client, tasks):
    msg = b"Choose a service: \n1 RPS \n2 TTT \n3 C4|send"
    while True:
        await co_send(msg, client)
        response = await co_recv(1024, client)
        print(response.decode(encoding="UTF-8"))
        if response == b"1":
            task: asyncio.Task = asyncio.create_task(serve_RPS(client))
            task.add_done_callback(tasks.discard)
            tasks.add(task)
            await co_send(b"You chose RPS|send", client)
            break
        elif response == b"2":
            task: asyncio.Task = asyncio.create_task(serve_TTT(client))
            task.add_done_callback(tasks.discard)
            tasks.add(task)
            await co_send(b"You chose TTT|send", client)
            break
        elif response == b"3":
            task: asyncio.Task = asyncio.create_task(serve_C4(client))
            task.add_done_callback(tasks.discard)
            tasks.add(task)
            await co_send(b"You chose C4|send", client)
            break
        else:
            msg = b"Invalid Option, choose a service: \n1 RPS \n2 TTT \n3 C4"

async def serve_RPS(client):
    while True:
        data = await co_recv(1024, client)
        print(f"Received {data} from {client}, RPS")
        options = ['rock', 'paper', 'scissors']
        result = rps(data.decode(encoding="UTF-8"), options[random.randint(0,2)])
        await co_send(bytes(f"{result}|send",encoding="UTF-8"), client)
        if data == "close":
            break

async def serve_TTT(client):
    while True:
        data = await co_recv(1024, client)
        print(f"Received {data} from {client}, TTT")
        await co_send(bytes(f"{data}|send",encoding="UTF-8"), client)
        if data == "close":
            break

async def serve_C4(client):
    while True:
        data = await co_recv(1024, client)
        print(f"Received {data} from {client}, C4")
        await co_send(bytes(f"{data}|send",encoding="UTF-8"), client)
        if data == "close":
            break

async def main():
    tasks = set()
    with socket.socket() as sock:
        sock.settimeout(0)
        sock.bind((ADDR, PORT))
        sock.listen()
        print(f"Server listening on {ADDR}:{PORT}")
        while True:
            client, addr = await co_accept(sock)
            print(f"connected to {addr}")
            task: asyncio.Task = asyncio.create_task(server_select(client, tasks))
            task.add_done_callback(tasks.discard)
            tasks.add(task)

if __name__ == "__main__":
    asyncio.run(main())
