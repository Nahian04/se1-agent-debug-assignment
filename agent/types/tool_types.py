from typing import Dict, Union, List, Optional
from pydantic import BaseModel

class CalcArgs(BaseModel):
    numbers: Optional[list[float]] = None
    operation: Optional[str] = None
    expr: Optional[str] = None

class TempArgs(BaseModel):
    cities: List[str]
    operation: str = "single"

class WeatherArgs(BaseModel):
    cities: List[str]

IntermediateValues = Dict[str, Union[str, float, Dict]]
