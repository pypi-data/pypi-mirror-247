from typing import TypedDict

class PolygonAggregate(TypedDict):
    c: float
    h: float
    l: float
    n: int
    o: float
    t: int
    v: int
    vw: float


PolygonAggregates = list[PolygonAggregate]
