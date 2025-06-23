from textual.widgets import Widget
from textual.reactive import reactive

from rich.panel import Panel
from rich.box import box


class Logs(Widget):
    def on_mount(self) -> None:
        self.panel = Panel("Stuff", title="Logs", border_style="white",
                           box=box.SQUARE)
        self.has_focus = reactive(False)

    def render(self) -> None:
        return self.panel
