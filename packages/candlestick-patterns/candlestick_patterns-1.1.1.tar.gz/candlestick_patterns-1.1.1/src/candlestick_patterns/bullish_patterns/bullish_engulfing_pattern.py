from ..pattern_abc import PatternSearcher


class BullishEngulfingPattern(PatternSearcher):
    def search_for_pattern_in_aggs(self) -> bool:
        previous_day_candle = self.aggs[1]
        today_candle = self.aggs[0]
        if (
            today_candle.close
            > today_candle.open  # Closing price > Opening price for the second candle
            and previous_day_candle.close
            < previous_day_candle.open  # Closing price < Opening price for the first candle
            and previous_day_candle.close
            < today_candle.open  # Previous closing price < Current opening price
            and previous_day_candle.open
            > today_candle.close  # Previous opening price > Current closing price
        ):
            return True
        else:
            return False
