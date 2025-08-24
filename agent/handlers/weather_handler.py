from typing import Optional, Dict, List
from .. import tools
from utils.logger import get_logger
from ..types.tool_types import WeatherArgs, IntermediateValues
from ..types.plan_types import WeatherResultType
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def handle_weather(
    args: WeatherArgs,
    intermediate_values: IntermediateValues
) -> Optional[WeatherResultType]:
    """
    Handle weather requests for one or more cities.

    Args:
        args (WeatherArgs): Arguments containing the 'cities' list.
        intermediate_values (IntermediateValues): Dictionary for storing intermediate results.

    Returns:
        Optional[WeatherResultType]: Weather result per city (dict) or single string if one city.
    
    Raises:
        Exception: Propagates any exception raised during weather lookup or processing.
    """
    
    logger.info("handle_weather called with args: %s", args.model_dump())

    try:
        cities: List[str] = args.cities

        if not cities:
            logger.warning("handle_weather called with empty cities list")
            return None

        if len(cities) == 1:
            result: str = tools.weather(cities[0])
        else:
            result: Dict[str, str] = {city.title(): tools.weather(city) for city in cities}

        intermediate_values["weather"] = result
        logger.info("handle_weather result for cities %s: %s", cities, result)

        return result

    except Exception:
        logger.exception(
            "Error in handle_weather with args: %s and intermediate_values: %s",
            args.model_dump(), intermediate_values
        )
        raise
