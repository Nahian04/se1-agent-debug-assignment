import re
from typing import List
from utils.logger import get_logger
from constants.miscellaneous_constants import FX_TOOL, CALC_TOOL
from constants.regex_constants import CURRENCY_OP_PATTERN
from ..types.plan_types import PlanStepsListType
from ..types.tool_types import CalcArgs, FXArgs
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def parse_currency(prompt: str) -> PlanStepsListType:
    """
    Parse a natural language prompt for currency conversion and return a list of tool steps.

    Args:
        prompt (str): User input containing currency conversion instructions.

    Returns:
        PlanStepsListType: A list of dictionaries, each describing a calc/fx tool step.

    Raises:
        Exception: If any unexpected error occurs during parsing.
    """

    logger.info("parse_currency called with prompt: %s", prompt)
    try:
        tools: PlanStepsListType = []

        match = re.search(CURRENCY_OP_PATTERN, prompt, re.IGNORECASE)
        if match:
            operation: str = match.group(1) or "single"
            numbers_text: str = match.group(2)
            numbers: List[float] = [float(n.replace(',', '')) for n in re.findall(r"\d+(?:\.\d+)?", numbers_text)]

            from_currency: str = match.group(3).upper()
            to_currency: str = match.group(4).upper()

            logger.debug(
                "Parsed operation: %s | Numbers: %s | From: %s | To: %s",
                operation, numbers, from_currency, to_currency
            )

            if len(numbers) > 1:
                # For multiple numbers, first calculate the aggregation and then convert
                tools.append({
                    "tool": CALC_TOOL,
                    "args": CalcArgs(numbers=numbers, operation=operation.lower()).model_dump()
                })
                tools.append({
                    "tool": FX_TOOL,
                    "args": FXArgs(amount=None, from_currency=from_currency, to_currency=to_currency).model_dump()
                })
            else:
                # Direct conversion for single number
                tools.append({
                    "tool": FX_TOOL,
                    "args": FXArgs(amount=numbers[0], from_currency=from_currency, to_currency=to_currency).model_dump()
                })

            logger.debug("Matched currency conversion tools: %s", tools)
        else:
            logger.info("No currency pattern matched for prompt: %s", prompt)

        logger.info("parse_currency extracted tools: %s", tools)
        return tools

    except Exception:
        logger.exception("Error in parse_currency with prompt: %s", prompt)
        raise
