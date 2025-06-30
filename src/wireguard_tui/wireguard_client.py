import socket


class WireGuardClient():
    """
    Class for communicating with the wiregaurd daemon. Acts as a client for
    the WireguardDaemon
    """
    SOCKET_PATH = "/run/wg-manager.sock"

    @classmethod
    def activate(cls, config: str) -> bool:
        """Activate a wireguard configuration"""
        return cls.send_message(f"up {config}")

    @classmethod
    def deactivate(cls, config: str) -> bool:
        """Deactivate a wireguard configuration"""
        return cls.send_message(f"down {config}")

    @classmethod
    def list(cls) -> bool:
        """List all available configs"""
        return cls.send_message("list").split("\n")

    @classmethod
    def show(cls, config: str) -> bool:
        """
        shows the public key, listening port, endpoint and other relevant
        information.
        """
        return cls.send_message(f"show {config}")

    @classmethod
    def send_message(cls, message: str) -> str:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(cls.SOCKET_PATH)
            s.sendall(message.encode())
            data = s.recv(1024).decode()
            return data


if __name__ == "__main__":
    WireGuardClient.list()
