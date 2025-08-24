from typing import Optional
from .. import tools
from utils.logger import get_logger
from ..types.tool_types import KBArgs, IntermediateValues
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def handle_kb(args: KBArgs, intermediate_values: IntermediateValues) -> Optional[str]:
    """
    Perform a knowledge-base lookup using the provided query.

    Args:
        args (KBArgs): Model containing the query string `q`.
        intermediate_values (IntermediateValues): Dictionary to store intermediate results.

    Returns:
        Optional[str]: Result of the KB lookup, or None if the query is empty.

    Raises:
        Exception: Propagates any unexpected errors during lookup.
    """

    logger.info("handle_kb called with args: %s", args)

    try:
        q_text: str = args.q
        
        if not q_text:
            logger.warning("handle_kb called without 'q' argument")
            return None

        result: str = tools.kb_lookup(q_text)
        logger.info("handle_kb result for query '%s': %s", q_text, result)

        intermediate_values["last_kb_result"] = result
        return result

    except Exception:
        logger.exception(
            "Error in handle_kb with args: %s and intermediate_values: %s", args, intermediate_values
        )
        raise
