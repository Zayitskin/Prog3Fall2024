from __future__ import annotations

import asyncio
import socket

async def co_accept(sock: socket.socket) -> tuple[socket.socket, str]:

    while True:
        try:
            return sock.accept()
        except BlockingIOError:
            await asyncio.sleep(0)

async def co_send(data: bytes, sock: socket.socket) -> int:

    while True:
        try:
            return sock.send(data)
        except BlockingIOError:
            await asyncio.sleep(0)

async def co_recv(size: int, sock: socket.socket) -> bytes:

    while True:
        try:
            return sock.recv(size)
        except BlockingIOError:
            await asyncio.sleep(0)
