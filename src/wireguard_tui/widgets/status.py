from textual.widget import Widget

from rich.panel import Panel
from rich import box


class Status(Widget):
    """
    Displays whether the selected tunnel is active or not and the associated
    IP address of the tunnel.
    """

    def render(self) -> None:
        content = "Active: True\nLocal interface IP's: 10.6.8.9"
        return Panel(content,
                     title="Status",
                     border_style=self.app.get_css_variables()["foreground"],
                     box=box.SQUARE,
                     expand=True)
