from textual.app import App, ComposeResult
from textual.widgets import Footer
from textual.screen import ModalScreen
from textual import events

from rich.panel import Panel

from src.widgets import TunnelSelect, TunnelInformation, Status


class ErrorModal(ModalScreen):
    def render(self) -> None:
        return Panel("An error occured")


class WireGuardApp(App):
    BINDINGS = [
        ("q", "quit", "quit"),
        ("space", "activate", "toggle tunnel")
    ]

    CSS_PATH = "src/app.tcss"

    def compose(self) -> ComposeResult:
        yield TunnelSelect()
        yield Status()
        yield TunnelInformation()
        yield Footer()
        yield ErrorModal()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"

    def on_key(self, event: events.Key) -> None:
        # self.query_one(RichLog).write(event)
        pass

    def key_j(self) -> None:
        # self.query_one(RichLog).write("move_down")
        self.query_one(TunnelSelect).move_down()

    def key_k(self) -> None:
        # self.query_one(RichLog).write("move_up")
        self.query_one(TunnelSelect).move_up()


if __name__ == "__main__":
    app = WireGuardApp()
    app.run()
