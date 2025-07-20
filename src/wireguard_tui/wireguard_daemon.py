import subprocess
import socket
import os

from typing import Type, Self


class WireGuardDaemon:
    """
    The WireGuardDaemon is a service is ran in the background that allows the
    TUI to necessary elevated commands in order to run. These commands include:

    - Listing available configurations
    - Returning information about the activate connection
    - Starting and stopping connections
    - Return status of Daemon (whether it is running or not)
    """
    SOCKET_PATH = "/run/wg-manager.sock"

    commands = {
        "up": lambda args: WireGuardDaemon.up(args[0]),
        "down": lambda args: WireGuardDaemon.down(args[0]),
        "list": lambda args: WireGuardDaemon.list(),
        "show": lambda args: WireGuardDaemon.show(args[0])
    }

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
        Returns a string that shows information about the interface such as
        listening port, endpoint, allowed ips, latest handshake and other
        things.

        The show command can also list all interfaces that are up if given
        "interfaces" as a interface.
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

            parts = data.strip().split()

            if not parts:
                return

            cmd, args = parts[0], parts[1:]

            if cmd in cls.commands:
                result = cls.commands[cmd](args)
                if result is not None:
                    conn.sendall(str(result).encode())
            else:
                conn.sendall(b"Unknown command")

    @classmethod
    def run(cls: Type[Self]) -> None:
        # Socket path for the AF_UINX address family
        MAXIMUM_CONNECTIONS = 1

        # Remove the socket path before socket bind
        if os.path.exists(cls.SOCKET_PATH):
            os.remove(cls.SOCKET_PATH)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(cls.SOCKET_PATH)
            os.chmod(cls.SOCKET_PATH, 0o666)
            server.listen(MAXIMUM_CONNECTIONS)

            print(f"daemon running {os.getpid()}")

            while True:
                conn, _ = server.accept()
                with conn:
                    cls.handler(conn)

    @classmethod
    def is_running(cls: Type[Self]) -> bool:
        """
        Checks whether the daemon can be opened. Will return False
        if the socket is not running and True if the daemon is running.
        """

        # Not enough permissions to run this
        # if os.path.exists(cls.SOCKET_PATH):
        #    print("socket path does not exist")
        #    return False

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(cls.SOCKET_PATH)
                return True
        except socket.error:
            print("cannot connect to socket")
            return False


def main():
    WireGuardDaemon.run()


if __name__ == "__main__":
    main()
