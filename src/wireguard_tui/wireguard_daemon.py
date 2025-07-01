import subprocess
import threading
import socket
import os


def handler(conn) -> None:
    print("client connected")
    while True:
        data = conn.recv(1024).decode().strip()

        if not data:
            print("Client disconnected")
            break

        if data.startswith("up "):
            print("down")
            profile = data.split()[1]
            command = subprocess.run(["wg-quick", "up", profile])
            conn.sendall(bytes(command.returncode))
        elif data.startswith("down "):
            print("down")
            profile = data.split()[1]
            subprocess.run(["wg-quick", "down", profile])
            conn.sendall(bytes(command.returncode))
        elif data == "list":
            configs = subprocess.run(["ls", "/etc/wireguard/"],
                                     capture_output=True, text=True)
            print("list: \n" + configs.stdout)
            conn.sendall(configs.stdout.encode())
        elif data.startswith("show"):
            profile = data.split()[1]
            print("profile: " + profile)
            info = subprocess.run(["wg", "show", profile],
                                  capture_output=True, text=True)
            print("show: \n" + info.stdout)
            conn.sendall(info.stdout.encode())


def run(socket_path: str):
    # Socket path for the AF_UINX address family
    MAXIMUM_CONNECTIONS = 1

    # Remove the socket path before socket bind
    if os.path.exists(socket_path):
        os.remove(socket_path)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(socket_path)
        os.chmod(socket_path, 0o666)
        server.listen(MAXIMUM_CONNECTIONS)

        print(f"daemon running {os.getpid()}")

        while True:
            conn, _ = server.accept()
            with conn:
                handler(conn)


if __name__ == "__main__":
    SOCKET_PATH = "/run/wg-manager.sock"
    run(SOCKET_PATH)
