# [MIT] Copyright (c) 2023 Michel Novus

import socket
import os
import os.path
import unittest
import threading
import time
from typing import Union
from .serializer import PyCoreObject, serialize, deserialize


class Server(object):
    """"""

    def __init__(
        self,
        socket_path: str,
        buffer_size: int = 65536,
    ) -> None:
        self.socket_path = socket_path
        self.buffer_size = buffer_size
        self._instance_in_context = False
        self._socket: Union[socket.socket, None] = None
        self._connection: Union[socket.socket, None] = None

    def __enter__(self):
        if os.path.exists(self.socket_path):
            raise FileExistsError(f"socket {self.socket_path} already exists")
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.bind(self.socket_path)
        self._socket.listen(1)
        self._instance_in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection is not None:
            self.close_connection()
        if self._socket is not None:
            self._close_server()

    def wait_connection(self) -> PyCoreObject:
        """Wait for client data."""
        if not self._instance_in_context:
            raise TypeError(
                "Server class is a ContextManager, use in 'with' statement!"
            )
        self._connection = self._socket.accept()[0]  # type:ignore
        data = self._connection.recv(self.buffer_size)
        data = deserialize(data)
        return data

    def reply(self, data: PyCoreObject) -> None:
        """Send data to client."""
        serialized_data = serialize(data)
        if len(serialized_data) > self.buffer_size:
            raise OverflowError()
        self._connection.sendall(serialized_data)  # type:ignore

    def close_connection(self) -> None:
        """Close current client connection."""
        self._connection.shutdown(socket.SHUT_RD)  # type:ignore
        self._connection.close()  # type:ignore
        self._connection = None

    def _close_server(self) -> None:
        """Close socket server."""
        self._socket.shutdown(socket.SHUT_RD)  # type:ignore
        self._socket.close()  # type:ignore
        os.unlink(self.socket_path)


def communicate(
    socket_path: str, data: PyCoreObject, buffer_size: int = 65536
) -> PyCoreObject:
    """It connects with a UNIX socket and sends data, waiting
    to receive a response.

    ### Exceptions:
    - FileNotFoundError: if socket not exists
    - ConnectionRefusedError: socket is busy or invalid
    - TimeoutError: socket invalid or connection is satured
    - InterruptedError: connection interrupted from outside
    - TypeError: if data is not PyCoreObject
    - JSONDecodeError: if data is not a valid JSON bytes
    - OverflowError: if serialized data is more than buffer_size
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as _socket:
        _socket.connect(socket_path)
        serialized_data = serialize(data)
        if len(serialized_data) > buffer_size:
            raise OverflowError(
                f"data length is too much big (max={buffer_size} bytes)"
            )
        _socket.send(serialized_data)
        response = deserialize(_socket.recv(buffer_size))
    return response


# ----------------------------------------------------------------------


class _TestIpc(unittest.TestCase):
    def setUp(self):
        time.sleep(0.05)  # Delay in opening and closing sockets between tests.
        self.socket_file = "/tmp/ipc_purepy.socket"
        self.listed_data = ["cadena", 20, None, True, False, 0.22]
        self.dict_data = {
            "clave": "éxito!",
            "valor": 0,
            "lista": self.listed_data,
            "algo": [True, True, False],
        }

    def test_client_server_simple_interaction(self):
        if os.path.exists(self.socket_file):
            os.unlink(self.socket_file)

        def new_server_thread():
            with Server(self.socket_file) as server:
                client_object = server.wait_connection()
                self.assertEqual(client_object, self.listed_data)
                server.reply(self.dict_data)
                server.close_connection()

        server_thread = threading.Thread(target=new_server_thread)
        server_thread.start()
        time.sleep(0.05)
        server_object = communicate(self.socket_file, self.listed_data)
        self.assertEqual(server_object, self.dict_data)
        server_thread.join(1)
