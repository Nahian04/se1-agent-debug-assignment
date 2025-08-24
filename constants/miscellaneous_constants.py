from typing import Dict, List, Callable, Union

TEMPERATURE_TOOL = "temperature"
WEATHER_TOOL = "weather"
CALC_TOOL = "calc"
KB_TOOL = "kb"
FX_TOOL = "fx"

# Default word-to-symbol mapping for arithmetic operations
WORD_OPS: Dict[str, str] = {
    "add": "+", "plus": "+", "sum": "+",
    "subtract": "-", "minus": "-",
    "multiply": "*", "times": "*",
    "divide": "/", "divided": "/"
}

# List of valid currencies
VALID_CURRENCIES: List[str] = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]

DEFAULT_CITY = "dhaka"
SUPPORTED_CITIES = {"paris", "london", "dhaka"}

FX_RATES: Dict[str, float] = {
    "usd_to_eur": 0.91
}

# Predefined temperatures for cities
CITY_TEMPS: dict[str, float] = {
    "paris": 18,
    "london": 17.0,
    "dhaka": 31,
    "amsterdam": 19.5
}

AGGREGATE_FUNCTIONS: Dict[str, Callable[[List[float]], Union[int, float]]] = {
    "average": lambda lst: round(sum(lst) / len(lst)),
    "avg": lambda lst: round(sum(lst) / len(lst)),
    "total": lambda lst: round(sum(lst)),
    "sum": lambda lst: round(sum(lst)),
    "maximum": max,
    "max": max,
    "minimum": min,
    "min": min,
}

WEATHER_DESCRIPTIONS: dict[str, str] = {
    "paris": "Mild and cloudy.",
    "london": "Cool and rainy.",
    "dhaka": "Hot and humid."
}