from typing import List
from polygon.rest.models.aggs import Agg


def is_hammer_with_downtrend(candle_data: List[Agg]) -> bool:
    # Check for a downtrend in the past 7 candles
    if all(candle_data[i].close < candle_data[i].open for i in range(-7, -1)):
        # Check for Hammer pattern
        if (
            candle_data[-1].close
            > candle_data[
                -1
            ].open  # Closing price > Opening price for the current candle
            and candle_data[-1].low
            < candle_data[
                -1
            ].open  # Lower shadow is at least twice the size of the body
            and candle_data[-1].low - candle_data[-1].open
            >= (candle_data[-1].close - candle_data[-1].open) / 2
        ):
            return True

    return False
