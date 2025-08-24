from typing import Union, Dict, List
from .. import tools
from utils.logger import get_logger
from ..types.tool_types import CalcArgs, IntermediateValues
from ..types.plan_types import CalcResultType
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

def _calc_with_city_temperatures(expr: str, temp_val_dict: Dict[str, float], intermediate_values: IntermediateValues) -> CalcResultType:
    """
    Case-1: Apply an expression to per-city temperature values.

    Args:
        expr (str): Expression to evaluate.
        temp_val_dict (Dict[str, float]): Mapping of cities to temperatures.
        intermediate_values (IntermediateValues): Shared state.

    Returns:
        CalcResultType: Updated temperature results as a string for single city or dict for multiple cities.
    """
    
    calc_results: Dict[str, float] = {}
    ops: List[str] = [op.strip() for op in expr.split("and")]
    for key, val in temp_val_dict.items():
        result: CalcResultType = val
        for op in ops:
            result: CalcResultType = tools.evaluate(f"{result}{op}")
        calc_results[key] = result

    intermediate_values["temperature"] = calc_results
    intermediate_values["last_calc_result"] = calc_results

    if len(calc_results) == 1:
        temperature: float = list(calc_results.values())[0]
        logger.info("handle_calc result: %s°C", temperature)
        return f"{temperature}°C"
    else:
        formatted_results: Dict[str, str] = {k.title(): f"{v}°C" for k, v in calc_results.items()}
        logger.info("handle_calc results: %s", formatted_results)
        return formatted_results


def _calc_with_numbers(numbers: List[float], operation: str, intermediate_values: IntermediateValues) -> CalcResultType:
    """
    Case-2: Perform an arithmetic operation on a list of numbers.

    Args:
        numbers (List[float]): List of numeric values.
        operation (str): Operation to perform (e.g., "sum", "avg").
        intermediate_values (IntermediateValues): Shared state.

    Returns:
        CalcResultType: Result of the calculation.
    """

    result: CalcResultType = tools.calc_numbers(numbers, operation)
    intermediate_values["last_calc_result"] = result
    logger.info("handle_calc result: %s", result)

    return result


def _calc_with_last_result(expr: str, intermediate_values: IntermediateValues) -> CalcResultType:
    """
    Case-3: Apply an expression to the last calculation result.

    Args:
        expr (str): Expression to evaluate.
        intermediate_values (IntermediateValues): Shared state containing the last result.

    Returns:
        CalcResultType: Result of the calculation.
    """

    base_value = intermediate_values.get("last_calc_result")
    result: CalcResultType

    if isinstance(base_value, dict):
        result = next(iter(base_value.values()))
    elif isinstance(base_value, (int, float)):
        result = float(base_value)
    else:
        result = 0.0

    ops: List[str] = [op.strip() for op in expr.split("and")]
    for op in ops:
        new_expr: str = f"{result} {op}" if result else f"{op}"
        result: CalcResultType = tools.evaluate(new_expr)

    intermediate_values["last_calc_result"] = result
    logger.info("handle_calc result: %s", result)
    return result

@track_latency(__name__)
@typechecked
def handle_calc(args: CalcArgs, intermediate_values: IntermediateValues) -> CalcResultType:
    """
    Route calculation requests to the appropriate handler.

    Depending on the provided arguments, this function delegates to:
      - `_calc_with_city_temperatures` for expressions on per-city temperatures,
      - `_calc_with_numbers` for operations on numeric lists,
      - `_calc_with_last_result` for expressions applied to the last result.

    Args:
        args (CalcArgs): Calculation arguments (numbers, operation, or expression).
        intermediate_values (IntermediateValues): Shared state across tool executions.

    Returns:
        CalcResultType: Result of the calculation (float, dict, str, or None).

    Raises:
        Exception: If any underlying calculation fails unexpectedly.
    """

    logger.info("handle_calc called with args: %s", args.model_dump())

    try:
        numbers: Union[List[float], None] = args.numbers
        operation: Union[str, None] = args.operation
        expr: Union[str, None] = args.expr
        temp_val_dict: Dict[str, float] = intermediate_values.get("temperature", {})
        
        if expr and temp_val_dict:
            return _calc_with_city_temperatures(expr, temp_val_dict, intermediate_values)
        elif numbers and operation:
            return _calc_with_numbers(numbers, operation, intermediate_values)
        elif expr:
            return _calc_with_last_result(expr, intermediate_values)
        else:
            logger.warning("handle_calc received args but no valid case matched: %s", args.model_dump())
            return None

    except Exception:
        logger.exception("Error occurred in handle_calc with args: %s", args.model_dump())
        raise
