from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label
from textual.screen import ModalScreen
from textual.containers import Container

from rich.panel import Panel
from rich import print

from .wireguard_client import WireGuardClient
from .wireguard_daemon import WireGuardDaemon
from .widgets import TunnelSelect, TunnelInformation


class ErrorModal(ModalScreen):
    def render(self) -> None:
        return Panel("An error occured")


class WireGuardApp(App):
    # Available bindings
    BINDINGS = [
        ("q", "quit", "quit"),
        ("space", "activate", "toggle tunnel")
    ]

    CSS_PATH = "./app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="content"):
            yield TunnelSelect(WireGuardClient.list())
            yield TunnelInformation()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"

    def key_j(self) -> None:
        # self.query_one(RichLog).write("move_down")
        self.query_one(TunnelSelect).move_down()

    def key_k(self) -> None:
        # self.query_one(RichLog).write("move_up")
        self.query_one(TunnelSelect).move_up()


def main():
    if (WireGuardDaemon.is_running()):
        app = WireGuardApp()
        app.run()
    else:
        print("[bold red]Cannot connect to WireGuardDaemon")
