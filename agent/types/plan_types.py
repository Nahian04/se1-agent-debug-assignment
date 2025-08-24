from typing import Dict, Union, List
from pydantic import BaseModel
from .tool_types import CalcArgs

class PlanStepModel(BaseModel):
    tool: str
    args: Union[CalcArgs]

AnswerResultType = Union[str, Dict[str, str], float, None]
CalcResultType = Union[str, Dict[str, str], float, None]
PlanStepDictType = Dict[str, Union[str, Dict[str, str]]]  
PlanStepsListType = List[PlanStepDictType]
