from textual.widget import Widget

from rich.panel import Panel
from rich.text import Text
from rich import box

from ..wireguard_client import WireGuardClient


class TunnelSelect(Widget):
    """Displays tunnels that can be selected"""

    def __init__(self):
        super().__init__()
        self.tunnels = self.get_tunnels()
        self.select_index = 0

    def render(self) -> None:
        return Panel(self.__convert_list_to_text(self.tunnels),
                     title="Tunnel Select",
                     border_style=self.app.get_css_variables()["primary"],
                     box=box.SQUARE,
                     expand=True)

    def get_tunnels(self) -> list:
        try:
            tunnels = WireGuardClient.list()
            return tunnels.split("\n")[:-1]
        except (Exception):
            return ["tunnel 1", "tunnel 2", "tunnel 3", "tunnel 4", "tunnel 5"]

    def move_up(self) -> None:
        if (self.select_index > 0):
            self.select_index -= 1
            self.refresh()

    def move_down(self) -> None:
        if (self.select_index < len(self.tunnels) - 1):
            self.select_index += 1
            self.refresh()

    def __convert_list_to_text(self, tunnels: list) -> Text:
        text = Text()
        for i in range(len(self.tunnels)):
            temp = Text(self.tunnels[i] + "\n")
            if i == self.select_index:
                temp.stylize("black on white")
            text += temp

        return text
