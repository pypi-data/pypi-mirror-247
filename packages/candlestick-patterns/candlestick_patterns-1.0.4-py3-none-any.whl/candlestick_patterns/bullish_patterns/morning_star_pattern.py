from polygon.rest.models.aggs import Agg


def is_morning_star(candle1: Agg, candle2: Agg, candle3: Agg) -> bool:
    if (
        candle3.close
        > candle3.open  # Closing price > Opening price for the third candle
        and candle3.close - candle3.open
        >= (candle3.open - candle3.close)
        / 2  # Body of the third candle is at least halfway up
        and candle2.close
        < candle2.open  # Closing price < Opening price for the second candle
        and candle2.open
        > candle3.close  # Opening price of the second candle > Closing price of the third candle
        and candle2.close
        > candle1.open  # Closing price of the second candle > Opening price of the first candle
        and candle1.close
        < candle1.open  # Closing price < Opening price for the first candle
    ):
        return True
    else:
        return False
