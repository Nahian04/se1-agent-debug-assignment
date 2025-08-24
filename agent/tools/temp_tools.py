from typing import List, Dict, Union
from constants.miscellaneous_constants import CITY_TEMPS, DEFAULT_CITY, AGGREGATE_FUNCTIONS
from utils.logger import get_logger
from typeguard import typechecked

logger = get_logger(__name__)

@typechecked
def temp(cities: List[str], operation: str = "single") -> Union[str, Dict[str, str]]:
    """
    Retrieve temperatures for given cities, either individually or using an aggregate operation.

    Args:
        cities (List[str]): List of city names.
        operation (str, optional): Operation type. 
            - "single" (default): Return temperatures for each city.  
            - "average" / "avg": Return the average temperature.  
            - "total" / "sum": Return the total temperature sum.  
            - "maximum" / "max": Return the maximum temperature.  
            - "minimum" / "min": Return the minimum temperature.  

    Returns:
        Dict[str, str]: Dictionary with city names and temperatures (or aggregated result).

    Raises:
        ValueError: If an unsupported operation is provided.
        Exception: For unexpected errors during processing.
    """

    logger.info("Starting temperature retrieval for cities: %s with operation: %s", cities, operation)

    try:
        temps: List[float] = []


        for city in cities:
            temp = CITY_TEMPS.get(city.lower())

            if temp:
                temps.append(temp)
            elif len(cities) == 1:
                temp = CITY_TEMPS.get(DEFAULT_CITY.lower())
                return f"Temperature data unavailable. Default for {DEFAULT_CITY.capitalize()}: {temp}°C"

        logger.info("Fetched temperatures: %s", dict(zip(cities, temps)))

        op: str = operation.lower()

        if op == "single":
            result: Dict[str, str] = {city.title(): f"{temp_val}°C" for city, temp_val in zip(cities, temps)}
            logger.info("Returning single temperatures: %s", result)
            return result

        if op in AGGREGATE_FUNCTIONS:
            result: Union[int, float] = AGGREGATE_FUNCTIONS[op](temps)
            logger.info("Aggregated result for operation '%s': %s", op, result)
            return {op.capitalize(): f"{int(result)}°C"}

        raise ValueError(f"Unknown operation: {operation}")

    except Exception:
        logger.error("Error retrieving temperatures for cities: %s with operation: %s", cities, operation, exc_info=True)
        return {}
