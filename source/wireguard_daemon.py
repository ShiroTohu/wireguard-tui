import subprocess
import socket
import os

# Socket path for the AF_UINX address family
SOCKET_PATH = "/run/wg-manager.sock"
MAXIMUM_CONNECTIONS = 1

# Remove the socket path before socket bind
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o666)
    server.listen()

    print("daemon is running")

    conn, _ = server.accept()
    with conn:
        while True:
            data = conn.recv(1024).decode().strip()

            if data.startswith("up "):
                profile = data.split()[1]
                command = subprocess.run(["wg-quick", "up", profile])
                conn.sendall(bytes(command.returncode))
            elif data.startswith("down "):
                profile = data.split()[1]
                subprocess.run(["wg-quick", "down", profile])
                conn.sendall(bytes(command.returncode))
            elif data == "list":
                configs = subprocess.run(["ls", "/etc/wireguard/"],
                                         capture_output=True, text=True)
                conn.sendall(configs.stdout.encode())
            elif data.startswith("watch"):
                profile = data.split()[1]
                info = subprocess.run(["watch", "wg", "show", profile],
                                      capture_output=True, text=True)
                conn.sendall(info.stdout.encode())
