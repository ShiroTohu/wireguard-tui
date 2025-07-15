import socket
from typing import Type, Self


class WireGuardClient():
    """
    Class for communicating with the wiregaurd daemon. Acts as a client for
    the WireguardDaemon
    """
    SOCKET_PATH = "/run/wg-manager.sock"

    @classmethod
    def activate(cls: Type[Self], config: str) -> bool:
        """Activate a wireguard configuration"""
        return cls.send_message(f"up {config}")

    @classmethod
    def deactivate(cls: Type[Self], config: str) -> bool:
        """Deactivate a wireguard configuration"""
        return cls.send_message(f"down {config}")

    @classmethod
    def list(cls: Type[Self]) -> bool:
        """List all available configs"""
        return cls.send_message("list").split("\n")[:-1]

    @classmethod
    def show(cls: Type[Self], config: str) -> bool:
        """
        shows the public key, listening port, endpoint and other relevant
        information.
        """
        return cls.send_message(f"show {config}")

    @classmethod
    def send_message(cls: Type[Self], message: str) -> str:
        """
        Helper method that sends a message to the server and returns the
        response. Useful for sending commands to the server
        """
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(cls.SOCKET_PATH)
            s.sendall(message.encode())
            data = s.recv(1024).decode()
            return data
