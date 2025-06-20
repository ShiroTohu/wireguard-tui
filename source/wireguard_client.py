import socket


class WireGuardClient():
    """
    Class for communicating with the wiregaurd daemon. Acts as a client for
    the WireguardDaemon
    """
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    SOCKET_PATH = "/run/wg-manager.sock"

    @classmethod
    def get_configs(cls):
        """Return a list of available wireguard configurations"""

        # This probably has to be initialized
        cls.client_socket.connect(cls.SOCKET_PATH)
        cls.client_socket.send('list')

    @classmethod
    def activate(cls, config: bytes) -> bool:
        """Activate a wireguard configuration"""
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(cls.SOCKET_PATH)
            s.sendall(b'activate ' + config)
            data = s.recv(1024)
            print(data)

    @classmethod
    def deactivate(cls, config: bytes) -> bool:
        """Deactivate a wireguard configuration"""
        cls.client_socket.send(b"deactivate " + config)


if __name__ == "__main__":
    WireGuardClient.activate(b"Blahaj")
