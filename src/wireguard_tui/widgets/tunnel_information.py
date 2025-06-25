from textual.widget import Widget

from rich.panel import Panel
from rich import box

from src.wireguard_client import WireGuardClient


class TunnelInformation(Widget):
    """TunnelInformation displays information about the tunnel"""

    def render(self) -> None:
        return Panel(self.get_information(),
                     title="Tunnel Information",
                     border_style="white", box=box.SQUARE,
                     expand=True)

    def get_information(self) -> str:
        try:
            information = WireGuardClient.show("jp-tyo-wg-002")
            return information
        except (Exception):
            return "Cannot find tunnel"
