# IPC PurePy

The package allow sent core Python objects between two likely independent 
Python processes using UNIX sockets.

It provides a Server class (`Server`), a Client function 
(`communicate`), and a `PyCoreObject` type alias.

### PyCoreObject alias:
It's a type alias defined as the union of the basic types of Python language
(`str`, `int`, `float`, `bool`, `None`) and common collections
(`list[PyCoreObject]` and `dict[str, PyCoreObject]`).  
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