import subprocess
import socket
import os

# Socket path for the AF_UINX address family
SOCKET_PATH = "/run/wg-manager.sock"
MAXIMUM_CONNECTIONS = 1

# Remove the socket path before socket bind
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
os.chmod(SOCKET_PATH, 0o660)
server.listen(MAXIMUM_CONNECTIONS)

while True:
    conn, _ = server.accept()
    with conn:
        data = conn.recv(1024).decode().strip()
        if data.startswith("connect "):
            profile = data.split()[1]
            subprocess.run(["wg-quick", "up", profile])
        elif data.startswith("disconnect "):
            profile = data.split()[1]
            subprocess.run(["wg-quick", "down", profile])
        elif data.startswith("list"):
            subprocess.run(["ls", "etc/wireguard/"])
