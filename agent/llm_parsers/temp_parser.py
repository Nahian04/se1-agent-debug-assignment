import re
from typing import List
from utils.logger import get_logger
from constants.regex_constants import TEMPERATURE_PATTERN, CITY_CLEAN_PATTERN, CITY_SPLIT_PATTERN
from constants.miscellaneous_constants import SUPPORTED_CITIES, TEMPERATURE_TOOL
from ..types.plan_types import PlanStepsListType
from ..types.tool_types import TempArgs
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def parse_temperature(prompt: str) -> PlanStepsListType:
    """
    Parse a natural language prompt for temperature queries and return a list of tool steps.

    Args:
        prompt (str): User input containing a temperature query.

    Returns:
        PlanStepsListType: A list of dictionaries, each describing a temperature tool step.

    Raises:
        Exception: If any unexpected error occurs during parsing.
        
    Notes:
        - Supports queries like "What is the temperature in Paris and London?".
        - Detects operations like average, total, maximum, minimum, etc.
        - Defaults to ["dhaka"] if no city is matched.
    """

    logger.info("parse_temperature called with prompt: %s", prompt)
    tools: PlanStepsListType = []


    try:
        if "temperature" not in prompt.lower():
            logger.info("Prompt does not contain 'temperature'; skipping parsing.")
            return tools

        match = re.search(TEMPERATURE_PATTERN, prompt, re.IGNORECASE) # Regex to detect temperature queries

        cities: List[str] = []
        temp_operation: str = "single"

        if match:
            temp_op_text = match.group(1)
            city_part = re.sub(CITY_CLEAN_PATTERN, "", match.group(2).lower())
            words = re.split(CITY_SPLIT_PATTERN, city_part)

            for city in SUPPORTED_CITIES:
                if city in words and city not in cities:
                    cities.append(city)

            if temp_op_text:
                temp_operation = temp_op_text.lower()
                logger.info("Detected temperature operation: %s", temp_operation)
        else:
            logger.info("No temperature regex match found in prompt.")
        
        if not cities:
            cities = [""]
            logger.info("No cities matched; defaulting to: %s", cities)

        # Append parsed tool step using Pydantic
        tools.append({
            "tool": TEMPERATURE_TOOL,
            "args": TempArgs(cities=cities, operation=temp_operation).model_dump()
        })

        logger.info("Finished parse_temperature. Tools: %s", tools)

    except Exception:
        logger.exception("Error parsing temperature from prompt: %s", prompt)
        raise

    return tools
