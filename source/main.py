import os

from textual.app import App, ComposeResult, Widget
from textual.widgets import ListView, Label
from textual.containers import Grid
from textual import events
from textual.screen import ModalScreen 

from rich import box
from rich.panel import Panel


class WireGuardDaemon():
    """Class for communicating with the wiregaurd daemon"""

    def __init__(self):
        """Initializes the connection"""
        pass

    @staticmethod
    def get_configs():
        """Return a list of available wireguard configurations"""
        try:
            path = "/etc/wireguard/"
            return os.listdir(path)
        except PermissionError:
            return "Cannot read /etc/wireguard. Permission denied. Please run as root to access this folder."

    @staticmethod
    def activate(config: str) -> bool:
        """Activate a wireguard configuration"""
        pass

    @staticmethod
    def deactivate(config: str) -> bool:
        """Deactivate a wireguard configuration"""
        pass


class FocusPanel(Widget):
    def on_mount(self) -> None:
        self.panel = Panel("Stuff", title="Tunnels", border_style="red",
                           box=box.SQUARE)

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
        ("tab", "next_panel", "Next Panel (Tab)")
    ]

    def compose(self) -> ComposeResult:
        yield Grid(
            TunnelsSelect(),
            Logs(),
            NetworkInformation(),
            TunnelInformation(),
        )

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.screen.styles.background = "transparent"
        self.focus_index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")

    def on_key(self, event: events.Key):
        if event.key == "tab":
            self.focus_index += 1

    def action_next_panel(self):
        self.focus_index += 1


if __name__ == "__main__":
    app = WireGuardApp()
    app.run()
