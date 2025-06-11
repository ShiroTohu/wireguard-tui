from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Label, Static
from textual.containers import Container
from rich.panel import Panel


class TunnelsSelect(Static):
    def render(self) -> Panel:
        return Panel("Stuff", title="Tunnels", border_style="white")


class WireguardApp(App):
    BINDINGS = [("q", "quit", "quit")]

    def compose(self) -> ComposeResult:
        yield TunnelsSelect()

    def on_mount(self) -> None:
        self.title = "Wireguard TUI"
        self.screen.styles.background = "black"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).text
        self.console.print(f"Selected: {selected}")


if __name__ == "__main__":
    app = WireguardApp()
    app.run()
