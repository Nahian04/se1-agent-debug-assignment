import re
from typing import List, Dict
from utils.logger import get_logger
from constants.regex_constants import BINARY_PATTERN, IMPERATIVE_PATTERN, PERCENT_PATTERN
from constants.miscellaneous_constants import WORD_OPS, CALC_TOOL
from ..types.plan_types import PlanStepsListType
from ..types.tool_types import CalcArgs
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

def _parse_percent(prompt: str) -> List[Dict]:
    """
    Parse percentage expressions like '10% of 50' in the prompt.

    Args:
        prompt (str): The user input containing percentage expressions.

    Returns:
        List[Dict]: A list of tool steps for percentage calculations.
    """

    tools: List[Dict] = []

    for num, val in re.findall(PERCENT_PATTERN, prompt):
        expr = f"{num}% of {val}"
        tools.append({"tool": CALC_TOOL, "args": CalcArgs(expr=expr).model_dump()})
        logger.debug("Matched percent expression: %s", expr)
    return tools


def _parse_binary(prompt: str) -> List[Dict]:
    """
    Parse binary expressions in the prompt, using either symbols (e.g., +, -, *, /)
    or word operators (e.g., 'plus', 'minus').

    Args:
        prompt (str): The user input containing binary expressions.

    Returns:
        List[Dict]: A list of tool steps for binary calculations.
    """
    
    tools: List[Dict] = []

    for n1, op, n2 in re.findall(BINARY_PATTERN, prompt, re.IGNORECASE):
        expr_op = WORD_OPS.get(op.lower(), op)  # Converting word operator to symbol
        expr = f"{n1} {expr_op} {n2}"
        tools.append({"tool": CALC_TOOL, "args": CalcArgs(expr=expr).model_dump()})
        logger.debug("Matched binary expression: %s", expr)
    return tools


def _parse_imperative(prompt: str) -> List[Dict]:
    """
    Parse imperative expressions like 'add 5' in the prompt.

    Args:
        prompt (str): The user input containing imperative instructions.

    Returns:
        List[Dict]: A list of tool steps for imperative calculations.
    """

    tools: List[Dict] = []
    
    expr_list: List[str] = []
    for op, val in re.findall(IMPERATIVE_PATTERN, prompt, re.IGNORECASE):
        expr_list.append(f"{WORD_OPS[op.lower()]} {val}")
    if expr_list:
        expr = " and ".join(expr_list)
        tools.append({"tool": CALC_TOOL, "args": CalcArgs(expr=expr).model_dump()})
        logger.debug("Matched imperative expression: %s", expr)
    return tools

@track_latency(__name__)
@typechecked
def parse_calc(prompt: str) -> PlanStepsListType:
    """
    Parse a natural language prompt for calculator operations and return a list of tool steps.

    Args:
        prompt (str): User input containing arithmetic instructions.

    Returns:
        PlanStepsListType: A list of dictionaries, each describing a calc tool step.

    Raises:
        Exception: If any unexpected error occurs during parsing.
    """

    logger.info("parse_calc called with prompt: %s", prompt)
    try:
        tools: PlanStepsListType = []

        tools.extend(_parse_percent(prompt)) # Parsing percentage expressions

        
        binary_tools = _parse_binary(prompt) # Parsing binary expressions (both words and symbols)
        tools.extend(binary_tools)

        if not binary_tools:
            tools.extend(_parse_imperative(prompt)) # Parsing imperative expressions if no binary expression found

        logger.info("parse_calc extracted tools: %s", tools)
        return tools

    except Exception:
        logger.exception("Error in parse_calc with prompt: %s", prompt)
        raise
