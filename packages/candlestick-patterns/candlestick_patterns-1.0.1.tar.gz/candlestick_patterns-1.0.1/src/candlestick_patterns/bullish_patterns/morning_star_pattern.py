from ..models import PolygonAggregate


def is_morning_star(
    candle1: PolygonAggregate, candle2: PolygonAggregate, candle3: PolygonAggregate
) -> bool:
    if (
        candle3["c"]
        > candle3["o"]  # Closing price > Opening price for the third candle
        and candle3["c"] - candle3["o"]
        >= (candle3["o"] - candle3["c"])
        / 2  # Body of the third candle is at least halfway up
        and candle2["c"]
        < candle2["o"]  # Closing price < Opening price for the second candle
        and candle2["o"]
        > candle3[
            "c"
        ]  # Opening price of the second candle > Closing price of the third candle
        and candle2["c"]
        > candle1[
            "o"
        ]  # Closing price of the second candle > Opening price of the first candle
        and candle1["c"]
        < candle1["o"]  # Closing price < Opening price for the first candle
    ):
        return True
    else:
        return False
