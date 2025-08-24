import re
from typing import List, Union
from ..types.plan_types import CalcResultType
from constants.regex_constants import AVERAGE_PATTERN, CLEAN_EXPRESSION_PATTERN
from constants.miscellaneous_constants import WORD_OPS
from utils.logger import get_logger
from typeguard import typechecked

logger = get_logger(__name__)

def _percent_of(expr: str) -> CalcResultType:
    """
    Calculate percentage expressions of the form 'X % of Y'.

    Args:
        expr (str): The input percentage expression, e.g., "10 % of 200".

    Returns:
        float: The calculated percentage result.

    Raises:
        Exception: If parsing fails and evaluation also fails.
    """

    logger.info("Calculating percent expression: %s", expr)
    try:
        left, right = expr.split("% of")
        x: float = float(left.strip())
        y: float = float(right.strip())
        result: float = (x / 100.0) * y
        logger.info("Percent calculation result: %s", result)
        return result
    except Exception:
        logger.error("Failed percent calculation for expr: %s. Falling back to eval.", expr, exc_info=True)
        try:
            result: float = eval(expr)
            logger.info("Eval fallback result: %s", result)
            return result
        except Exception:
            logger.error("Eval fallback failed for expr: %s", expr, exc_info=True)
            return 0.0

@typechecked
def evaluate(expr: str) -> CalcResultType:
    """
    Evaluate mathematical expressions in string form.

    Supports percentage, addition, average, and basic arithmetic.

    Args:
        expr (str): The mathematical expression, e.g., "average of 10 and 20".

    Returns:
        float: The evaluated result.

    Raises:
        Exception: If evaluation fails after preprocessing.
    """

    logger.info("Evaluating expression: %s", expr)
    try:
        e: str = expr.lower().replace("what is", "").strip()
        e = re.sub(CLEAN_EXPRESSION_PATTERN, "", e)

        if "% of" in e:
            return _percent_of(e)

        # Replacing operator words like add, divide with corresponding symbols
        for word, symbol in WORD_OPS.items():
            e = e.replace(f"{word} ", symbol)

        e = e.replace(" to the ", " + ")

        match = re.search(AVERAGE_PATTERN, e)
        if match:
            a, b = match.groups()
            e = str((int(a) + int(b)) / 2)
            logger.info("Average computed: %s", e)

        result: float = eval(e)
        logger.info("Evaluated result: %s", result)
        return float(f"{result:.1f}")
    
    except ZeroDivisionError as zde:
        logger.error("Division by zero in expression: %s", expr, exc_info=True)
        raise

    except Exception as e:
        logger.error("Error evaluating expression: %s", expr, exc_info=True)
        return None


@typechecked
def calc_numbers(numbers: List[Union[int, float]], operation: str) -> CalcResultType:
    """
    Perform numeric list operations: sum, average, max, min.

    Args:
        numbers (List[Union[int, float]]): List of numbers to operate on.
        operation (str): Operation to perform - "sum", "average", "max", or "min".

    Returns:
        float: The result of the operation.

    Raises:
        ValueError: If an unsupported operation is provided.
        Exception: For any unexpected errors during calculation.
    """

    logger.info("Calculating numbers: %s with operation: %s", numbers, operation)
    try:
        if not numbers:
            logger.info("Empty numbers list provided. Returning 0.")
            return 0.0

        op: str = operation.lower()
        if op in ["sum", "total"]:
            result: float = sum(numbers)
        elif op in ["average", "avg"]:
            result = sum(numbers) / len(numbers)
        elif op in ["maximum", "max"]:
            result = max(numbers)
        elif op in ["minimum", "min"]:
            result = min(numbers)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        logger.info("Result of %s operation: %s", operation, result)
        return float(result)

    except Exception:
        logger.error("Error in calc_numbers with operation: %s", operation, exc_info=True)
        return None
