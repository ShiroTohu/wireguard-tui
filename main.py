from textual.app import App, ComposeResult
from textual.widgets import ListView, Label, RichLog
from textual.screen import ModalScreen
from textual import events

from rich.panel import Panel

from source.widgets import Logs, TunnelSelect

"""
class FocusPanel(Widget):
    can_focus = True

    def on_mount(self) -> None:
        self.panel = Panel("temp", title="Tunnels",
                           border_style="white", box=box.SQUARE)
        self.has_focus = reactive(False)

    def render(self) -> Panel:
        return self.panel

    def on_focus(self) -> Panel:
        self.panel.border_style = "red"
        self.has_focus = True

    def on_blur(self) -> Panel:
        self.panel.border_style = "white"
        self.has_focus = False
"""


class ErrorModal(ModalScreen):
    def render(self) -> None:
        return Panel("An error occured")


class WireGuardApp(App):
    BINDINGS = [
        ("q", "quit", "quit")
    ]

    CSS_PATH = "source/app.tcss"

    def compose(self) -> ComposeResult:
        yield TunnelSelect()
        yield RichLog()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.focus_index = 0

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)

    def key_j(self) -> None:
        self.query_one(TunnelSelect).move_down()
        self.query_one(RichLog).write("move_down")

    def key_k(self) -> None:
        self.query_one(TunnelSelect).move_up()
        self.query_one(RichLog).write("move_up")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")


if __name__ == "__main__":
    app = WireGuardApp()
    app.run()
