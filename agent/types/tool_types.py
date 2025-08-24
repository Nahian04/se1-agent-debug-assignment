from typing import Dict, Union, List, Optional
from pydantic import BaseModel

class CalcArgs(BaseModel):
    numbers: Optional[list[float]] = None
    operation: Optional[str] = None
    expr: Optional[str] = None

class FXArgs(BaseModel):
    amount: Optional[float] = None
    from_currency: str = None
    to_currency: str = None

class TempArgs(BaseModel):
    cities: List[str]
    operation: str = "single"

class WeatherArgs(BaseModel):
    cities: List[str]

class KBArgs(BaseModel):
    q: str = None
    
class KBEntry(BaseModel):
    name: str
    summary: str

class KBData(BaseModel):
    entries: List[KBEntry]

IntermediateValues = Dict[str, Union[str, float, Dict]]
