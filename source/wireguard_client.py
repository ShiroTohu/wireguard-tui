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

    @staticmethod
    def activate(config: str) -> bool:
        """Activate a wireguard configuration"""
        pass

    @staticmethod
    def deactivate(config: str) -> bool:
        """Deactivate a wireguard configuration"""
        pass
