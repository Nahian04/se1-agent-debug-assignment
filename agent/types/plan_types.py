from typing import Dict, Union, List
from pydantic import BaseModel
from .tool_types import CalcArgs, KBArgs, TempArgs, WeatherArgs

class PlanStepModel(BaseModel):
    tool: str
    args: Union[CalcArgs, KBArgs, TempArgs, WeatherArgs]

AnswerResultType = Union[str, Dict[str, str], float, None]
CalcResultType = Union[str, Dict[str, str], float, None]
TempResultType = Union[str, float, Dict[str, str], None]
WeatherResultType = Union[str, Dict[str, str], None]
PlanStepDictType = Dict[str, Union[str, Dict[str, str]]]  
PlanStepsListType = List[PlanStepDictType]
