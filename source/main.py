from textual.app import App, ComposeResult, Widget
from textual.widgets import ListView, Label, Footer
from textual import events

from rich import box
from rich.panel import Panel


class FocusPanel(Widget):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="red",
                     box=box.SQUARE)

    def on_focus(self) -> None:
        return None


class TunnelsSelect(FocusPanel):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="red",
                     box=box.SQUARE)


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


class WireguardApp(App):
    BINDINGS = [
        ("q", "quit", "quit"),
        ("tab", "next_panel", "Next Panel (Tab)")
    ]

    def compose(self) -> ComposeResult:
        yield TunnelsSelect()
        yield Logs()
        yield NetworkInformation()
        yield TunnelInformation()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.screen.styles.background = "transparent"
        self.focus_index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")

    def on_key(self, event: events.Key):
        if event.key == "tab":
            self.focus_index = self.focus_index + 1

    def action_next_panel():
        pass


if __name__ == "__main__":
    app = WireguardApp()
    app.run()
