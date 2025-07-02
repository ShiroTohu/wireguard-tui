import subprocess
import socket
import os
from typing import Type, Self


class WireGuardDaemon:
    @staticmethod
    def up(interface: str) -> int:
        """enable a wireguard interface"""
        command = subprocess.run(["wg-quick", "up", interface])
        return command.returncode

    @staticmethod
    def down(interface: str) -> int:
        """disable a wireguard interface"""
        command = subprocess.run(["wg-quick", "down", interface])
        return command.returncode

    @staticmethod
    def list() -> str:
        """
        return a list of available interfaces this includes
        .conf at the end since it's just listing the /etc/wireguard/
        directory
        """
        configs = subprocess.run(["ls", "/etc/wireguard/"],
                                 capture_output=True, text=True)
        return configs.stdout

    @staticmethod
    def show(interface: str) -> str:
        """
        return a string that shows information about the interface such as
        listening port, endpoint, allowed ips latest handshake and other
        things.
        """
        info = subprocess.run(["wg", "show", interface],
                              capture_output=True, text=True)
        return info.stdout

    @classmethod
    def handler(cls: Type[Self], conn: socket.socket) -> None:
        print("client connected")
        while True:
            data = conn.recv(1024).decode().strip()

            if not data:
                print("Client disconnected")
                break

            if data.startswith("up "):
                interface = data.split()[1]
                command = cls.up(interface)
                conn.sendall(bytes(command))
            elif data.startswith("down "):
                interface = data.split()[1]
                cls.down(interface)
                conn.sendall(bytes(command))
            elif data == "list":
                interfaces = cls.list()
                conn.sendall(interfaces.encode())
            elif data.startswith("show"):
                interface = data.split()[1]
                cls.show(interface)
                conn.sendall(interface.encode())

    @classmethod
    def run(cls: Type[Self], socket_path: str):
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
