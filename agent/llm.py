from typing import List
from pydantic import ValidationError
from constants.tool_constants import PARSERS, TOOL_MODELS
from .types.plan_types import PlanStepModel
from utils.logger import get_logger
from typeguard import typechecked
from utils.latency_tracker import track_latency

logger = get_logger(__name__)


@track_latency(__name__)
@typechecked
def call_llm(prompt: str) -> List[PlanStepModel]:
    """
    Parse a prompt into a sequence of tool execution steps.

    The prompt is processed by multiple parsers, each producing candidate
    tool steps. Parsed steps are validated against their Pydantic models 
    and combined into a final plan.

    Args:
        prompt (str): Input query or instruction.

    Returns:
        List[PlanStepModel]: Validated plan steps ready for execution.

    Raises:
        ValueError: If a step has no corresponding args model.
        ValidationError: If a step's arguments fail Pydantic validation.
        Exception: If any parser fails unexpectedly.
    """

    p: str = prompt.lower()
    logger.info("Received LLM prompt: %s", p)

    tools: List[PlanStepModel] = []

    for name, parser in PARSERS.items():
        try:
            result_dicts: List[dict] = parser(p)

            # Converting dictionaries to Pydantic models with the correct args type
            result: List[PlanStepModel] = []
            for step_dict in result_dicts:
                tool_name: str = step_dict["tool"]
                args_model = TOOL_MODELS.get(tool_name)

                if not args_model:
                    raise ValueError(f"No args model defined for tool {tool_name}")
            
                try:
                    parsed_args = args_model.model_validate(step_dict.get("args", {}))
                    result.append(PlanStepModel(tool=tool_name, args=parsed_args))
                except ValidationError as e:
                    logger.error("ValidationError: %s", e)
                
            if result:
                tools.extend(result)

            logger.info("Parsed %s tools: %s", name, result)
        except Exception:
            logger.exception("Error parsing %s tools", name)

    logger.info("Final tools plan: %s", tools)
    return tools
