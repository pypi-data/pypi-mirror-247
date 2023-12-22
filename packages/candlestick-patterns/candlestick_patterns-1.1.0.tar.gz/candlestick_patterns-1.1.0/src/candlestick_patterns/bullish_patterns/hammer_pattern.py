from ..pattern_abc import PatternSearcher


class HammerPattern(PatternSearcher):
    def search_for_pattern_in_aggs(self) -> bool:
        today_candle = self.aggs[-1]
        if all(self.aggs[i].close < self.aggs[i].open for i in range(-8, -1)):
            # Check for Hammer pattern
            if (
                today_candle.close > today_candle.open
                and today_candle.low < today_candle.open
                and today_candle.low - today_candle.open
                >= (today_candle.close - today_candle.open) / 2
            ):
                return True

        return False
