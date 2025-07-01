from textual.widget import Widget

from rich.panel import Panel
from rich import box


class NetworkInformation(Widget):
    """Using a graph NetworkInformation displays the network traffic"""

    def render(self) -> None:
        return Panel("",
                     title="Network - 10.10.4.36",
                     border_style=self.app.get_css_variables()["foreground"],
                     box=box.SQUARE,
                     expand=True)
