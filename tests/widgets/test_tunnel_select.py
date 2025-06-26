import pytest

from wireguard_tui.app import WireGuardApp
from wireguard_tui.widgets import TunnelSelect


@pytest.mark.asyncio
async def test_navigation():
    "Test application navigation"
    app = WireGuardApp()
    async with app.run_test() as pilot:
        await pilot.press("j")  # Down
        assert app.query_one(TunnelSelect).select_index == 1

        await pilot.press("k")  # Up
        assert app.query_one(TunnelSelect).select_index == 0
