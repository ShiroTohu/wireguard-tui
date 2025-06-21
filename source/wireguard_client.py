import socket


class WireGuardClient():
    """
    Class for communicating with the wiregaurd daemon. Acts as a client for
    the WireguardDaemon
    """
    SOCKET_PATH = "/run/wg-manager.sock"

    @classmethod
    def get_configs(cls):
        """Return a list of available wireguard configurations"""

        # This probably has to be initialized
        cls.client_socket.connect(cls.SOCKET_PATH)
        cls.client_socket.send('list')

    @classmethod
    def activate(cls, config: str) -> bool:
        """Activate a wireguard configuration"""
        return cls.send_message(f"up {config}")

    @classmethod
    def deactivate(cls, config: str) -> bool:
        """Deactivate a wireguard configuration"""
        return cls.send_message(f"down {config}")

    @classmethod
    def send_message(cls, message: str) -> str:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(cls.SOCKET_PATH)
            s.sendall(message.encode())
            data = s.recv(1024).decode()
            print(data)
            return data


if __name__ == "__main__":
    WireGuardClient.activate("Blahaj")
