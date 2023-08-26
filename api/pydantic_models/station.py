from pydantic import BaseModel, ConfigDict
from pydantic.types import Decimal

class Station(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    latitude: Decimal
    longtitude: Decimal
    flag: str
