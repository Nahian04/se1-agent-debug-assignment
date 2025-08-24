from utils.logger import get_logger
from constants.miscellaneous_constants import KB_TOOL
from ..types.plan_types import PlanStepsListType
from ..types.tool_types import KBArgs
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def parse_kb(prompt: str) -> PlanStepsListType:
    """
    Parse a natural language prompt for knowledge-base queries and return a list of tool steps.

    Args:
        prompt (str): User input containing a knowledge-base query.

    Returns:
        PlanStepsListType: A list of dictionaries, each describing a kb tool step.

    Raises:
        Exception: If any unexpected error occurs during parsing.
        
    Notes:
        - Supports prompts like "Who is <name>?".
    """

    logger.info("parse_kb called with prompt: %s", prompt)
    try:
        tools: PlanStepsListType = []

        # For pattern: "Who is <name>?"
        if "who is" in prompt.lower():
            name = prompt.lower().split("who is", 1)[1].strip().rstrip("?").strip()
            logger.debug("Extracted knowledge base query: %s", name)
            if name:
                tools.append({
                    "tool": KB_TOOL,
                    "args": KBArgs(q=name).model_dump()
                })
            else:
                logger.warning("Found 'who is' pattern but no name extracted from prompt: %s", prompt)
        else:
            logger.info("No knowledge base pattern matched for prompt: %s", prompt)

        logger.info("parse_kb extracted tools: %s", tools)
        return tools

    except Exception:
        logger.exception("Error in parse_kb with prompt: %s", prompt)
        raise
