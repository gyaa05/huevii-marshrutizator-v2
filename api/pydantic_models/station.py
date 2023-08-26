from pydantic import BaseModel, ConfigDict
from pydantic.types import Decimal

class CreateStation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    latitude: Decimal
    longtitude: Decimal
    flag: str

class GetStation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    latitude: Decimal
    longtitude: Decimal
    flag: str
    status: str
