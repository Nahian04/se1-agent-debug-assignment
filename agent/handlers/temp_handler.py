import re
from typing import Optional, List
from .. import tools
from utils.logger import get_logger
from ..types.plan_types import TempResultType
from constants.regex_constants import NUMERIC_TEMPERATURE_PATTERN
from ..types.tool_types import TempArgs, IntermediateValues
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def handle_temp(
    args: TempArgs,
    intermediate_values: IntermediateValues
) -> Optional[TempResultType]:
    """
    Handle temperature requests using the provided arguments.

    Args:
        args (TempArgs): Arguments containing 'cities' list and 'operation' string.
        intermediate_values (IntermediateValues): Dictionary for storing intermediate results.

    Returns:
        Optional[TempResultType]: The temperature result, or None if cities list is empty.

    Raises:
        Exception: Propagates any exception raised during temperature lookup or processing.
    """

    logger.info("handle_temp called with args: %s", args.model_dump())
    
    try:
        cities: List[str] = args.cities
        operation: str = args.operation
        temperature: TempResultType

        if not cities:
            logger.warning("handle_temp called with empty cities list")
            return None

        result: TempResultType = tools.temp(cities, operation)

        if isinstance(result, dict):

            cleaned_result = {k: float(str(v).replace("°C", "")) for k, v in result.items()}
            intermediate_values["temperature"] = cleaned_result

            if len(result) == 1:
                temperature = list(result.values())[0]
                logger.info("handle_calc result: %s", temperature)
                return f"{temperature}"
        
            
        elif isinstance(result, str):
            match = re.search(NUMERIC_TEMPERATURE_PATTERN, result)

            if match:
                temperature = float(match.group())
            else:
                temperature = None
            intermediate_values["temperature"] = temperature
        else:
            intermediate_values["temperature"] = result

        logger.info(
            "handle_temp result for cities %s with operation '%s': %s",
            cities, operation, result
        )
        
        return result

    except Exception:
        logger.exception(
            "Error in handle_temp with args: %s and intermediate_values: %s",
            args.model_dump(), intermediate_values
        )
        raise
