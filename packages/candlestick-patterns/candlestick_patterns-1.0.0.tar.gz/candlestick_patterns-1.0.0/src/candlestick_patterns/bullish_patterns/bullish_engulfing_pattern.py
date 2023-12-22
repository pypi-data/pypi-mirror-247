from ..models import PolygonAggregate


def is_bullish_engulfing(candle1: PolygonAggregate, candle2: PolygonAggregate) -> bool:
    if (
        candle2["c"]
        > candle2["o"]  # Closing price > Opening price for the second candle
        and candle1["c"]
        < candle1["o"]  # Closing price < Opening price for the first candle
        and candle1["c"]
        < candle2["o"]  # Previous closing price < Current opening price
        and candle1["o"]
        > candle2["c"]  # Previous opening price > Current closing price
    ):
        return True
    else:
        return False
