import pytest

from textual.app import App, ComposeResult

from wireguard_tui.app import WireGuardApp
from wireguard_tui.widgets import TunnelSelect


class SelectApp(App):
    """Test Application to store widget"""

    def compose(self) -> ComposeResult:
        yield TunnelSelect(["Option 1", "Option 2", "Option 3"])

    def key_j(self) -> None:
        # self.query_one(RichLog).write("move_down")
        self.query_one(TunnelSelect).move_down()

    def key_k(self) -> None:
        # self.query_one(RichLog).write("move_up")
        self.query_one(TunnelSelect).move_up()


@pytest.mark.asyncio
async def test_navigation():
    "Test application navigation"
    app = SelectApp()
    async with app.run_test() as pilot:
        await pilot.press("j")  # Down
        assert app.query_one(TunnelSelect).select_index == 1

        await pilot.press("k")  # Up
        assert app.query_one(TunnelSelect).select_index == 0
