from web_server import create_app
from storage.sockets import socket_io

app = create_app()

if __name__ == "__main__":
    socket_io.run(app)
