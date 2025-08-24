from typing import Optional
from constants.miscellaneous_constants import WEATHER_DESCRIPTIONS
from utils.logger import get_logger
from typeguard import typechecked

logger = get_logger(__name__)

@typechecked
def weather(city: str) -> str:
    """
    Retrieve the weather description for a given city.

    Args:
        city (str): The name of the city.

    Returns:
        str: A weather description if found in the predefined list, otherwise "Weather data unavailable." and default for Dhaka will be shown.

    Raises:
        Exception: If an unexpected error occurs during lookup.
    """

    logger.info("Starting weather lookup for city: '%s'", city)
    default_city: str = "dhaka"
    try:
        c: str = (city or "").strip().lower()
        description: Optional[str] = WEATHER_DESCRIPTIONS.get(c)
        if c not in WEATHER_DESCRIPTIONS:
            description: str = f"Weather data unavailable. Default for {default_city.capitalize()}: {WEATHER_DESCRIPTIONS.get(default_city)}"
            logger.info("City '%s' not found in descriptions. Using default: '%s'", city, description)
        else:
            logger.info("Found weather description for '%s': '%s'", city, description)
        return description
    except Exception:
        logger.error("Error retrieving weather for city: '%s'", city, exc_info=True)
        return "Weather data unavailable."