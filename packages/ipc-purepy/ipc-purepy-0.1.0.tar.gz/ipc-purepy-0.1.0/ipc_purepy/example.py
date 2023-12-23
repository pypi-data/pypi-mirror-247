# [MIT] Copyright (c) 2023 Michel Novus
"""Example of IPC PurePy. Execute with $ python3 -m ipc_purepy.example"""

from time import sleep
from threading import Thread
from random import choice
from ipc_purepy import Server, communicate

SOCKET = "/tmp/ipc_purepy.socket"


def server_thread():
    food = ["piza", "pan", "manzana", "pomelo", "helado", "fideos", "huevos"]
    with Server(SOCKET) as server:
        while True:
            client_data = server.wait_connection()
            if client_data == "exit":
                server.reply("closing server")
                # server.close_connection()
                # If the connection is not explicitly closed here, it is done
                # automatically when the server is closed when leaving the loop.
                break  # exits and does not run again server.wait_connection()
            print(client_data)
            server.reply(f"A random food: {choice(food)}")
            server.close_connection()
    # Here the server and any client connection is closed automatically


if __name__ == "__main__":
    thread = Thread(target=server_thread)
    # Uses another thread to emulate another Python "instance" (the simple way).
    thread.start()
    sleep(0.05)  # Needs a moment to make some system calls

    print(communicate(SOCKET, "First message, choise a food"))
    sleep(1)
    print(communicate(SOCKET, "Second message, choise a food"))
    sleep(1)
    print(communicate(SOCKET, "Thirt message, choise a food"))
    sleep(1)
    print(communicate(SOCKET, "exit"))
