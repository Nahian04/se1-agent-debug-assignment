import re
from typing import List
from utils.logger import get_logger
from constants.regex_constants import WEATHER_PATTERN, CITY_CLEAN_PATTERN, CITY_SPLIT_PATTERN
from constants.miscellaneous_constants import SUPPORTED_CITIES, WEATHER_TOOL
from ..types.plan_types import PlanStepsListType
from ..types.tool_types import WeatherArgs
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def parse_weather(prompt: str) -> PlanStepsListType:
    """
    Parse a natural language prompt for weather queries and return a list of tool steps.

    Args:
        prompt (str): User input containing a weather query.

    Returns:
        PlanStepsListType: A list of dictionaries, each describing a weather tool step.
    
    Raises:
        Exception: If any unexpected error occurs during parsing.
    """

    logger.info("parse_weather called with prompt: %s", prompt)
    tools: PlanStepsListType = []

    try:
        if "weather" not in prompt.lower():
            logger.info("Prompt does not contain 'weather'; skipping parsing.")
            return tools

        match = re.search(WEATHER_PATTERN, prompt, re.IGNORECASE) # Regex to detect weather queries

        cities: List[str] = []

        if match:
            after_weather = re.sub(CITY_CLEAN_PATTERN, "", match.group(1).lower())
            words = re.split(CITY_SPLIT_PATTERN, after_weather)
            for city in SUPPORTED_CITIES:
                if city in words and city not in cities:
                    cities.append(city)

            logger.info("Detected cities in prompt: %s", cities if cities else "None")
        else:
            logger.info("No weather regex match found in prompt.")

        if not cities:
            cities = [""]
            logger.info("No cities matched; defaulting to: %s", cities)

        # Append parsed tool step using Pydantic
        tools.append({
            "tool": WEATHER_TOOL,
            "args": WeatherArgs(cities=cities).model_dump()
        })

        logger.info("Finished parse_weather. Tools: %s", tools)

    except Exception:
        logger.exception("Error parsing weather from prompt: %s", prompt)
        raise

    return tools
