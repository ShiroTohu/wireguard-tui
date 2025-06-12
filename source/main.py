from textual.app import App, ComposeResult, Widget
from textual.widgets import ListView, Label, Static

from rich import box
from rich.panel import Panel


class TunnelsSelect(Static):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="red",
                     box=box.SQUARE)


class Logs(Widget):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="white",
                     box=box.SQUARE)


class TunnelInformation(Widget):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Tunnels", border_style="white", box=box.SQUARE)


class NetworkInformation(Widget):
    def render(self) -> Panel:
        return Panel("Information about current configuration",
                     title="Tunnels", border_style="white", box=box.SQUARE)


class WireguardApp(App):
    BINDINGS = [("q", "quit", "quit")]

    def compose(self) -> ComposeResult:
        yield TunnelsSelect()
        yield Logs()
        yield NetworkInformation()
        yield TunnelInformation()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.screen.styles.background = "transparent"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")


if __name__ == "__main__":
    app = WireguardApp()
    app.run()
