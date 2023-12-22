from polygon.rest.models.aggs import Agg


def is_bullish_engulfing(candle1: Agg, candle2: Agg) -> bool:
    if (
        candle2.close
        > candle2.open  # Closing price > Opening price for the second candle
        and candle1.close
        < candle1.open  # Closing price < Opening price for the first candle
        and candle1.close
        < candle2.open  # Previous closing price < Current opening price
        and candle1.open
        > candle2.close  # Previous opening price > Current closing price
    ):
        return True
    else:
        return False
