from __future__ import annotations

from .base import Ad, Connector, Side


class _UnimplementedP2P(Connector):
    """Placeholder for exchanges whose P2P endpoint hasn't been reverse-engineered
    and wired up yet. Raises clearly instead of silently returning no data."""

    def _unimplemented(self):
        raise NotImplementedError(
            f"{self.name} P2P connector not implemented yet — "
            f"see docs/ANALYSIS.md for known-viable exchanges and docs/ARCHITECTURE.md for the interface to implement."
        )

    async def fetch_ads(self, asset: str, fiat: str, side: Side, rows: int = 20) -> list[Ad]:
        self._unimplemented()


class BitgetP2P(_UnimplementedP2P):
    name = "bitget"


class HtxP2P(_UnimplementedP2P):
    name = "htx"


class GateioP2P(_UnimplementedP2P):
    name = "gateio"


class MexcP2P(_UnimplementedP2P):
    name = "mexc"


class NoonesP2P(_UnimplementedP2P):
    name = "noones"


class BitpapaP2P(_UnimplementedP2P):
    name = "bitpapa"


class LocalcoinswapP2P(_UnimplementedP2P):
    name = "localcoinswap"
