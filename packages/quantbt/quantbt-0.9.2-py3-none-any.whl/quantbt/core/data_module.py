import numpy as np
from numba import float64
from typing import Optional, List
from quantbt.core.enums import DataType, TradeSizeType

from numba.experimental import jitclass
from quantbt.core.specs_nb import data_specs

from quantbt.core.calculate_entry_price import calculate_entry_price
from quantbt.core.calculate_exit_price import calculate_exit_price


# pyright: reportGeneralTypeIssues=false
@jitclass(data_specs)
class DataModule:
    def __init__(
        self,
        close: List[float],
        data_type=DataType.OHLC.value,
        date: Optional[List[int]] = None,
        open: Optional[List[float]] = None,
        high: Optional[List[float]] = None,
        low: Optional[List[float]] = None,
        volume: Optional[List[float]] = None,
        bid: Optional[List[float]] = None,
        ask: Optional[List[float]] = None,
        initial_capital=100000.0,
        default_trade_size=-1,
        trade_size_type=TradeSizeType.PERCENTAGE.value,
        slippage=0.0,
    ) -> None:
        if date is not None:
            self.date: List[int] = date

        # PRICE DATA
        if data_type == DataType.OHLC.value:
            if open is not None:
                self.open: List[float] = open
            if high is not None:
                self.high: List[float] = high
            if low is not None:
                self.low: List[float] = low
            if close is not None:
                self.close: List[float] = close
        else:
            if bid is not None:
                self.bid: List[float] = bid
                self.close = bid
            if ask is not None:
                self.ask: List[float] = ask
            if bid is None or ask is None:
                raise ValueError("Please provide both Bid AND Ask")
        self.data_type: int = data_type

        if volume is not None:
            self.volume: List[float] = volume

        # PORTFOLIO
        length = len(self.close)
        self.equity = np.full(length, np.inf, dtype=np.float32)
        self.equity[0] = initial_capital

        self.initial_capital = float64(initial_capital)
        self.final_value = float64(initial_capital)
        self.total_pnl = float64(0.0)

        # SLIPPAGE
        self.slippage: float = slippage

        # Trade Sizing
        self.default_trade_size: float = default_trade_size
        self.trade_size_type: int = trade_size_type

    def get_data_at_index(self, index):
        date = self.date[index]
        close = self.close[index]
        high = self.high[index]
        low = self.low[index]
        if self.data_type == DataType.OHLC.value:
            return date, close, low, high
        else:
            return date, close, self.bid[index], self.ask[index]

    # ============================================================================= #
    #                               HELPER FUNCTIONS                                  #
    # ============================================================================= #
    # def reconcile_equity(self):

    # ============================================================================= #
    #                               SIZE FUNCTIONS                                  #
    # ============================================================================= #
    def get_trade_size(self, index):
        equity = self.equity[index - 1]
        price_value = self.close[index]
        # TODO this function needs to make sure we have enough equity to trade
        if self.trade_size_type == TradeSizeType.PERCENTAGE.value:
            return self.default_trade_size * equity / price_value
        else:
            return self.default_trade_size

    def calculate_entry_price(self, i, direction):
        price_value = 0
        bid = 0
        ask = 0
        if self.data_type == DataType.OHLC.value:
            price_value = self.close[i]
        else:
            bid = self.bid[i]
            ask = self.ask[i]
        return calculate_entry_price(self.slippage, direction, price_value, bid, ask)

    def get_entry_price(self, i, direction):
        bid: float = 0
        ask: float = 0
        price: float = 0
        if self.data_type == DataType.OHLC.value:
            price = self.close[i]
        else:
            bid = self.bid[i]
            ask = self.ask[i]

        return calculate_entry_price(self.slippage, direction, price, bid, ask)

    def update_equity(self, i, closed_pnl, floating_pnl):
        self.equity[i] = self.initial_capital + closed_pnl + floating_pnl
