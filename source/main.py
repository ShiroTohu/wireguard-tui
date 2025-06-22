from textual.app import App, ComposeResult
from textual.widgets import ListView, Label
from textual.widget import Widget
from textual.containers import Grid
from textual.screen import ModalScreen

from rich import box
from rich.panel import Panel


class FocusPanel(Widget):
    def on_mount(self) -> None:
        self.panel = Panel("temp", title="Tunnels",
                           border_style="red", box=box.SQUARE)

    def render(self) -> Panel:
        return self.panel

    def on_focus(self) -> None:
        return None


class TunnelsSelect(FocusPanel):
    def render(self) -> Panel:
        return self.panel


class Logs(FocusPanel):
    def render(self) -> Panel:
        return Panel("Stuff", title="Logs", border_style="white",
                     box=box.SQUARE)


class TunnelInformation(FocusPanel):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Information", border_style="white", box=box.SQUARE)


class NetworkInformation(FocusPanel):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Network Traffic", border_style="white", box=box.SQUARE)


class ErrorModal(ModalScreen):
    def render(self) -> Panel:
        return Panel("An error occured")


class WireGuardApp(App):
    BINDINGS = [
        ("q", "quit", "quit"),
        ("tab", "next_panel", "Next Panel"),
        ("shift+tab", "last_panel", "Last Panel")
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
