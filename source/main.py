from textual.app import App, ComposeResult
from textual.widgets import ListView, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import ModalScreen

from rich import box
from rich.panel import Panel


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


class TunnelsSelect(FocusPanel):
    def render(self) -> Panel:
        return self.panel


class Logs(FocusPanel):
    def on_mount(self) -> None:
        self.panel = Panel("Stuff", title="Logs", border_style="white",
                           box=box.SQUARE)


class TunnelInformation(FocusPanel):
    def on_mount(self) -> None:
        self.panel = Panel("Stuff", title="Logs", border_style="white",
                           box=box.SQUARE)


class NetworkInformation(FocusPanel):
    def on_mount(self) -> None:
        self.panel = Panel("Stuff", title="Logs", border_style="white",
                           box=box.SQUARE)


class ErrorModal(ModalScreen):
    def render(self) -> None:
        return Panel("An error occured")


class WireGuardApp(App):
    BINDINGS = [
        ("q", "quit", "quit")
    ]

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield TunnelsSelect(id="tunnel_select")
        yield NetworkInformation()
        yield TunnelInformation()
        yield Logs()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.focus_index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")

    def action_next_panel(self):
        # the focus index cannot go above the number of panels
        self.focus_index += 1

    def action_last_panel(self):
        # the focus index cannot go below zero
        if (self.focus_index > 0):
            self.focus_index -= 1


if __name__ == "__main__":
    app = WireGuardApp()
    app.run()
