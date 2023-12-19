from ttxt.base import baseFuturesExchange, baseSpotExchange
from ttxt.exchanges.gateFutures import gateFutures
from ttxt.exchanges.bybitFutures import bybitFutures
from ttxt.exchanges.bingx import bingx

exchanges = [
    "gateFutures",
    "bybitFutures",
    "bingx"
]

base = [
    "baseFuturesExchange",
    "baseSpotExchange"
]

_all__ =  exchanges + base