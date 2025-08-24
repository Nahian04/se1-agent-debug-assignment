from typing import List, Optional
from constants.tool_constants import TOOL_HANDLERS, TOOL_MODELS
from .llm import call_llm
from utils.logger import get_logger
from .types.tool_types import IntermediateValues
from .types.plan_types import PlanStepModel, AnswerResultType
from typeguard import typechecked, TypeCheckError
from utils.latency_tracker import track_latency

logger = get_logger(__name__)

@track_latency(__name__)
@typechecked
def answer(q: str) -> AnswerResultType:
    """
    Process a natural language query by generating and executing a tool plan.

    The query is passed to the LLM to produce a plan. Each step is validated
    and dispatched to the corresponding handler. Intermediate results are shared,
    and the final tool's output is returned.

    Args:
        q (str): Input query.

    Returns:
        Returns:
        AnswerResultType: Final result from the executed plan. Can be a string, a float, or None if execution fails or the plan is invalid.

    Raises:
        ValueError: If a step has no corresponding args model or handler.
        TypeCheckError: If a handler receives arguments of an invalid type.
        Exception: If any handler execution fails unexpectedly.
    """

    try:
        plan_raw: Optional[List[PlanStepModel]] = call_llm(q) # Raw LLM output (list of dicts)
        plan: Optional[List[PlanStepModel]] = None

        if plan_raw and isinstance(plan_raw, list):
            plan = [PlanStepModel.model_validate(step) for step in plan_raw] # Parsing each step into a Pydantic model
        logger.info("Generated plan: %s", plan)
    except Exception:
        logger.exception("Failed to generate plan from LLM")
        return str(None)

    if plan:
        intermediate_values: IntermediateValues = {}
        result: AnswerResultType = ""

        for step in plan:
            tool_name: str = step.tool

            args_model = TOOL_MODELS.get(tool_name)

            if not args_model:
                raise ValueError(f"No args model defined for tool {tool_name}")
                
            handler = TOOL_HANDLERS.get(tool_name)
            
            if not handler:
                raise ValueError(f"No handler found for tool {tool_name}")
            
            args = args_model.model_validate(step.args)
            
            logger.info("Executing tool: %s with args: %s", tool_name, args.model_dump())

            try:
                result = handler(args, intermediate_values)
                logger.info("Tool %s executed successfully, result: %s", tool_name, result)
            except TypeCheckError as tce:
                logger.error("TypeError: %s", tce)
                print("TypeError:", tce)
                return None
            except ZeroDivisionError as zde:
                logger.error("ValueError: %s", zde)
                print("ZeroDivisionError:", zde)
                return None
            except ValueError as ve:
                logger.error("ValueError: %s", ve)
                print("ValueError:", ve)
                return None
            except Exception as e:
                logger.exception("Error executing tool: %s with args: %s", tool_name, args.model_dump())
                return None

        logger.info("Final result: %s", result)
        return result

    logger.warning("Invalid or empty plan returned: %s", plan)
    return None
