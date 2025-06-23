from textual.app import App, ComposeResult
from textual.widgets import ListView, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import ModalScreen

from rich import box
from rich.panel import Panel

from source.widgets import Logs

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

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Logs()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.focus_index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")


if __name__ == "__main__":
    app = WireGuardApp()
    app.run()
