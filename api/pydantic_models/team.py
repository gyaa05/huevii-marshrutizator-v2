from pydantic import BaseModel, ConfigDict

class RegisterTeam(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    token: str
    stations: list[int]

class LoginInTeam(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str

class RegisterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str

class TeamInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    status: str
    cur_station: int | None = None