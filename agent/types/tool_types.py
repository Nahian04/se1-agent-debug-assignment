from typing import Dict, Union, Optional
from pydantic import BaseModel

class CalcArgs(BaseModel):
    numbers: Optional[list[float]] = None
    operation: Optional[str] = None
    expr: Optional[str] = None

IntermediateValues = Dict[str, Union[str, float, Dict]]
