from textual.widget import Widget
from textual.reactive import reactive

from rich.panel import Panel
from rich.text import Text
from rich import box

from source.wireguard_client import WireGuardClient


class TunnelSelect(Widget):
    """Displays tunnels that can be selected"""

    def __init__(self):
        super().__init__()
        self.tunnels = self.get_tunnels()
        self.select_index = 0

    def on_mount(self) -> None:
        self.panel = Panel(self.__convert_list_to_text(self.tunnels),
                           title="Tunnel Select",
                           border_style="red", box=box.SQUARE,
                           expand=True)
        self.has_focus = reactive(False)

    def render(self) -> None:
        return self.panel

    def get_tunnels(self) -> list:
        return ["tunnel 1", "tunnel 2", "tunnel 3", "tunnel 4", "tunnel 5"]

    def __convert_list_to_text(self, tunnels: list) -> Text:
        text = Text()
        for i in range(len(self.tunnels)):
            temp = Text(self.tunnels[i] + "\n")
            if i == self.select_index:
                temp.stylize("black on white")
            text += temp

        return text
