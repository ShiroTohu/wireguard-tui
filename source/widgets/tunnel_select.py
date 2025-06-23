from textual.widget import Widget
from textual.reactive import reactive

from rich.panel import Panel
from rich import box


class TunnelSelect(Widget):
    """Displays tunnels that can be selected"""
    can_focus = True

    def on_mount(self) -> None:
        self.panel = Panel("Select tunnel", title="Tunnel Select",
                           border_style="white", box=box.SQUARE)
        self.has_focus = reactive(False)

    def render(self) -> None:
        return self.panel
