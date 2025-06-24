import subprocess
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
            print("list")
            configs = subprocess.run(["ls", "/etc/wireguard/"],
                                     capture_output=True, text=True)
            conn.sendall(configs.stdout.encode())
        elif data.startswith("show"):
            print("show")
            profile = data.split()[1]
            info = subprocess.run(["wg", "show", profile],
                                  capture_output=True, text=True)
            conn.sendall(info.stdout.encode())


def main():
    # Socket path for the AF_UINX address family
    SOCKET_PATH = "/run/wg-manager.sock"
    MAXIMUM_CONNECTIONS = 1

    # Remove the socket path before socket bind
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(SOCKET_PATH)
        os.chmod(SOCKET_PATH, 0o666)
        server.listen(MAXIMUM_CONNECTIONS)

        print("daemon is running...")

        while True:
            conn, _ = server.accept()
            with conn:
                handler(conn)


if __name__ == "__main__":
    main()
