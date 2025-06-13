import os

from textual.app import App, ComposeResult, Widget
from textual.widgets import ListView, Label
from textual import events

from rich import box
from rich.panel import Panel


class WireGuard():
    @staticmethod
    def get_configs():
        try:
            path = "/etc/wireguard/"
            return os.listdir(path)
        except PermissionError:
            return "None"


class FocusPanel(Widget):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="red",
                     box=box.SQUARE)

    def on_focus(self) -> None:
        return None


class TunnelsSelect(FocusPanel):
    def render(self) -> Panel:
        # TODO: keep in mind that the panel cannot render lists, only strings
        return Panel(WireGuard.get_configs(), title="Tunnels",
                     border_style="red", box=box.SQUARE)


class Logs(FocusPanel):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="white",
                     box=box.SQUARE)


class TunnelInformation(FocusPanel):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Tunnels", border_style="white", box=box.SQUARE)


class NetworkInformation(FocusPanel):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Tunnels", border_style="white", box=box.SQUARE)


class WireGuardApp(App):
    BINDINGS = [
        ("q", "quit", "quit"),
        ("tab", "next_panel", "Next Panel (Tab)")
    ]

    def compose(self) -> ComposeResult:
        yield TunnelsSelect()
        yield Logs()
        yield NetworkInformation()
        yield TunnelInformation()

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
