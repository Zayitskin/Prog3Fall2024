import random
import asyncio
import socket

from games import rps
from games import ttt
from games import connect

from sock_coro import co_accept
from sock_coro import co_recv
from sock_coro import co_send

ADDR = ""
PORT = 1234
clients = {}

def client_connect(username):
    clients[username] = len(clients.keys())+1
    print(clients.get(username))

async def server_select(client, tasks, username):
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
            task: asyncio.Task = asyncio.create_task(serve_C4(client, username))
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

async def serve_TTT(client1):
    while True:
        board = "_" * 9
        end = False
        counter = 0
        await co_recv(1024, client1)
        while not end:
            # if counter % 2 == 0:
            current_client = client1 
            # else:
            #     current_client = client2
            await co_send(bytes(f"{board}|print ttt",encoding="UTF-8"), current_client)
            await co_send(bytes(f"Choose your move|send",encoding="UTF-8"), current_client)
            move = await co_recv(1024, current_client)
            print(f"Received {move} from {current_client}, TTT")
            print(board)
            stats = ttt(board, int(move), counter)
            board = stats[1]
            if stats[0] is True:
                # if counter % 2 == 0:
                #     winner = client1 
                #     loser = client2 
                # else:
                #     winner = client2
                #     loser = client1 
                #     await co_send(bytes(f"You won :)",encoding="UTF-8"), winner)
                #     await co_send(bytes(f"You Lost :(",encoding="UTF-8"), loser)
                await co_send(bytes(f"{board}|print ttt",encoding="UTF-8"), current_client)
                end = True
            counter += 1

async def serve_C4(client, username):
    global_board = [
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_'
    ]
    board = list(global_board)
    while True:
        while True:
            data = await co_recv(1024, client)
            if data in [str(x+1).encode(encoding="UTF-8") for x in range(7)]:
                break
            await co_send(b"Enter a valid column|send", client)
        print(f"Received {data} from {client}, C4")
        state = connect(board, data, clients.get(username))
        if isinstance(state, bytes):
            await co_send(state, client)
            continue
        if data == "close":
            break
        board = state
        # is win statement here
        row = ""
        for i in range(len(board)):
            row += board[i] + " "
            if (i+1) % 7 == 0:
                row += "|wait"
                await co_send(bytes(row, encoding="UTF-8"), client)
                await asyncio.sleep(0.001)
                row = ""
        row += "|send"
        await co_send(bytes(row, encoding="UTF-8"), client)


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
            username = None
            while True:
                username = await co_recv(1024, client)
                if username:
                    username = username.decode(encoding="UTF-8")
                    break
            if not clients.get(username):
                client_connect(username)
            task = asyncio.create_task(server_select(client, tasks, username))
            task.add_done_callback(tasks.discard)
            tasks.add(task)

if __name__ == "__main__":
    asyncio.run(main())
