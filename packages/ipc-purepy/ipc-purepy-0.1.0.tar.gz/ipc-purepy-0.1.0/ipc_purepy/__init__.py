# [MIT] Copyright (c) 2023 Michel Novus
"""
# IPC PurePy
The package allow sent core Python objects between two likely independent 
Python processes using UNIX sockets.

It provides a Server class (Server), a Client function 
(communicate), and a PyCoreObject type alias.

### PyCoreObject alias:
It's a type alias defined as the union of the basic types of Python language
(str, int, float, bool, None) and common collections
(list[PyCoreObject] and dict[str, PyCoreObject]).  
The dict type key must be are str type and value are PyCoreObject.

### function is_pycoreobject(object: Any) -> bool:
This recursive function allows to check if the object passed to it 
is a valid PyCoreObject.

### class Server(socket_path: str):
The class defines the server socket as a context handler. Through the 
wait_connection() method it waits for some external connection and returns 
the PyCoreObject sent to it.  
The connection to the client is expected to be closed with the 
close_connection() method.  
Server class implements the reply() method that allows to send a 
PyCoreObject to the client if the connection is alive.

### function communicate(socket_path: str, data: PyCoreObject) -> PyCoreObject:
Client endpoint to communicate with the server socket, send data to 
server socket and expect receive a response from it.

## Example: (execute directly with $python3 -m ipc_purepy.example)
# --------------------------------------------------------------------------- #
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

# --------------------------------------------------------------------------- #
"""

from .ipc import Server, communicate
from .serializer import PyCoreObject, is_pycoreobject
