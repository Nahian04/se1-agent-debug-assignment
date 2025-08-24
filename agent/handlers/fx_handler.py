from typing import Dict
from .. import tools
from utils.logger import get_logger
from ..types.plan_types import FxResultType
from ..types.tool_types import FXArgs, IntermediateValues
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def handle_fx(args: FXArgs, intermediate_values: IntermediateValues) -> FxResultType:
    """
    Perform foreign exchange conversion using the provided arguments.

    If `amount` is not provided, the function attempts to use the last calculation
    result from `intermediate_values`. The result is stored in `intermediate_values`
    under the key 'last_fx_result'.

    Args:
        args (FXArgs): Input arguments containing 'amount', 'from_currency', and 'to_currency'.
        intermediate_values (IntermediateValues): Dictionary holding intermediate results from previous computations.

    Returns:
        FxResultType: The converted amount as a float.

    Raises:
        ValueError: If required parameters (amount, from_currency, to_currency) are missing.
        Exception: Any exception raised by `tools.fx_convert` is propagated after logging.
    """
    
    logger.info("handle_fx called with args: %s", args.model_dump())

    try:
        amount: float | None = args.amount
        from_currency: str | None = args.from_currency
        to_currency: str | None = args.to_currency

        # Fallback to last_calc_result if amount not provided
        if amount is None:
            last_value = intermediate_values.get("last_calc_result")
            if isinstance(last_value, (int, float)):
                amount = float(last_value)
            elif isinstance(last_value, dict):
                # Take first value if last_calc_result is a dict
                amount = next(iter(last_value.values()))
            logger.info("Using last_calc_result as amount: %s", amount)

        if amount is None or from_currency is None or to_currency is None:
            raise ValueError("Missing required FX parameters")

        result: float = tools.fx_convert(amount, from_currency, to_currency)
        logger.info(
            "FX conversion result: %s %s -> %s = %s", amount, from_currency, to_currency, result
        )

        intermediate_values["last_fx_result"] = result
        return result

    except Exception:
        logger.exception(
            "Error in handle_fx with args: %s and intermediate_values: %s",
            args.model_dump(),
            intermediate_values,
        )
        raise
