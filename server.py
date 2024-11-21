import random
import asyncio
import socket
import json

from games import rps
from games import ttt
from games import connect

from sock_coro import co_accept
from sock_coro import co_recv
from sock_coro import co_send

ADDR = "127.0.0.1"
PORT = 1234

clients = {"Luke":{"Noah":{"TTT":(0,0,0),"C4":(0,0,0),"RPS":(0,0,0)}},
           "Noah":{"Luke":{"TTT":(0,0,0),"C4":(0,0,0),"RPS":(0,0,0)}}
          }

    

def client_connect(username):
    for name in clients:
        clients[name][username] = {"TTT":(0,0,0),"C4":(0,0,0),"RPS":(0,0,0)}
    clients[username] = {name:{"TTT":(0,0,0),"C4":(0,0,0),"RPS":(0,0,0)} for name in clients}

async def server_select(client, tasks, username):
    msg = b"Choose a service: \n1 RPS \n2 TTT \n3 C4\n4 WDTV|send"
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
            await co_send(b"You chose C4|wait", client)
            break
        # elif response == b"4":
        #     task: asyncio.Task = asyncio.create_task(serve_WDTV(client, username))
        #     task.add_done_callback(tasks.discard)
        #     tasks.add(task)
        #     await co_send(b"You chose C4|wait", client)
        #     break
        else:
            msg = b"Invalid Option, choose a service: \n1 RPS \n2 TTT \n3 C4\n4 WDTV"

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

async def serve_C4(client1, client2, player1, player2):
    global_board = [
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_',
    '_', '_', '_', '_', '_', '_', '_'
    ]
    board = list(global_board)
    players = [player1, player2]
    clients = [client1, client2]
    active = 0
    while True:
        active_player = players[active]
        active_client = clients[active]
        row = ""
        for i in range(len(board)):
            row += board[i] + " "
            if (i+1) % 7 == 0:
                row += "|wait"
                await co_send(bytes(row, encoding="UTF-8"), active_client)
                await asyncio.sleep(0.001)
                row = ""
        await co_send(bytes(row, encoding="UTF-8"), active_client)
        while True:
            data = await co_recv(1024, client1)
            if data == b"board" or data in [str(x+1).encode(encoding="UTF-8") for x in range(7)]:
                break
            await co_send(b"Enter a valid column|send", active_client)
        if data == b"board":
            continue
        print(f"Received {data} from {client1}, C4")
        state = connect(board, data, clients.get(active_player))
        if isinstance(state, bytes):
            await co_send(state, active_client)
            continue
        if data == "close":
            break
        board = state
        active = (active + 1) % 2
        # is win statement here
    
async def do_save():
    print(clients)
    with open("client.txt", "w") as f:
        json.dump(clients, f)

async def main():
    global clients
    tasks = set()
    with open("client.txt", "r") as f:
        clients = json.load(f)
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
            await do_save()

if __name__ == "__main__":
    asyncio.run(main())
