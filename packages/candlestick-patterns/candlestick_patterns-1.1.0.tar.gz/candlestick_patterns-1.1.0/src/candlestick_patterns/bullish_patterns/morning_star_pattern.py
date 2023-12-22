from ..pattern_abc import PatternSearcher


class MorningStarPattern(PatternSearcher):
    def search_for_pattern_in_aggs(self) -> bool:
        candle1 = self.aggs[-3]
        candle2 = self.aggs[-2]
        candle3 = self.aggs[-1]
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
