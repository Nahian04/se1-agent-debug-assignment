from typing import Dict

CALC_TOOL = "calc"

# Default word-to-symbol mapping for arithmetic operations
WORD_OPS: Dict[str, str] = {
    "add": "+", "plus": "+", "sum": "+",
    "subtract": "-", "minus": "-",
    "multiply": "*", "times": "*",
    "divide": "/", "divided": "/"
}
