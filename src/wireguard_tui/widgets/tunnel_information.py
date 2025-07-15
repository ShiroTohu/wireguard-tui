from textual.widget import Widget

from rich.panel import Panel
from rich import box

from ..wireguard_client import WireGuardClient


class TunnelInformation(Widget):
    """TunnelInformation displays information about the tunnel"""

    def render(self) -> None:
        return Panel(self.get_information(),
                     title="Tunnel Information",
                     border_style=self.app.get_css_variables()["foreground"],
                     box=box.SQUARE,
                     expand=True)

    def get_information(self) -> str:
        """Sends a request to the socket to return tunnel information"""
        try:
            information = WireGuardClient.show("jp-tyo-wg-002")  # test configuration
            return information
        except (Exception):
            return "Cannot find tunnel"
