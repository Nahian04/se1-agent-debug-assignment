from typing import List, Callable, Dict, Type
from pydantic import BaseModel
from agent.llm_parsers import parse_weather, parse_temperature, parse_calc
from agent.types.tool_types import CalcArgs, TempArgs, WeatherArgs
from agent.handlers import handle_calc, handle_temp, handle_weather
from constants.miscellaneous_constants import TEMPERATURE_TOOL, WEATHER_TOOL, CALC_TOOL


# Each parser returns a list of dicts that can be parsed into PlanStepModel
PARSERS: Dict[str, Callable[[str], List[dict]]] = {
    WEATHER_TOOL: parse_weather,
    TEMPERATURE_TOOL: parse_temperature,
    CALC_TOOL: parse_calc,
}

# Map tool names to their specific Pydantic args models
TOOL_MODELS: Dict[str, Type[BaseModel]] = {
    CALC_TOOL: CalcArgs,
    WEATHER_TOOL: WeatherArgs,
    TEMPERATURE_TOOL: TempArgs,
}

TOOL_HANDLERS: Dict[str, Callable] = {
    CALC_TOOL: handle_calc,
    WEATHER_TOOL: handle_weather,
    TEMPERATURE_TOOL: handle_temp,
}