from ..models import PolygonAggregates

def is_hammer_with_downtrend(candle_data: PolygonAggregates) -> bool:
    # Check for a downtrend in the past 7 candles
    if all(candle_data[i]["c"] < candle_data[i]["o"] for i in range(-7, -1)):
        # Check for Hammer pattern
        if (
            candle_data[-1]["c"]
            > candle_data[-1][
                "o"
            ]  # Closing price > Opening price for the current candle
            and candle_data[-1]["l"]
            < candle_data[-1][
                "o"
            ]  # Lower shadow is at least twice the size of the body
            and candle_data[-1]["l"] - candle_data[-1]["o"]
            >= (candle_data[-1]["c"] - candle_data[-1]["o"]) / 2
        ):
            return True

    return False
