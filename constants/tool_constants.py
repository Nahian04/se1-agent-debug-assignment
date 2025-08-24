from typing import List, Callable, Dict, Type
from pydantic import BaseModel
from agent.llm_parsers import parse_temperature, parse_calc
from agent.types.tool_types import CalcArgs, TempArgs
from agent.handlers import handle_calc, handle_temp
from constants.miscellaneous_constants import TEMPERATURE_TOOL, CALC_TOOL


# Each parser returns a list of dicts that can be parsed into PlanStepModel
PARSERS: Dict[str, Callable[[str], List[dict]]] = {
    TEMPERATURE_TOOL: parse_temperature,
    CALC_TOOL: parse_calc,
}

# Map tool names to their specific Pydantic args models
TOOL_MODELS: Dict[str, Type[BaseModel]] = {
    CALC_TOOL: CalcArgs,
    TEMPERATURE_TOOL: TempArgs,
}

TOOL_HANDLERS: Dict[str, Callable] = {
    CALC_TOOL: handle_calc,
    TEMPERATURE_TOOL: handle_temp,
}