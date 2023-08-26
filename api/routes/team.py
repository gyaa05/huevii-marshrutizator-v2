from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from models.db_session import get_session
from descriptions.team import *
from pydantic_models.team import RegisterTeam, LoginInTeam, RegisterOut, TeamInfo
from models.team import Team
from auth.auth_handler import sign_jwt

router = APIRouter()

@router.post("/register", summary="Register new team", operation_id="register-new-team",
             description=register_new_team_description, response_model=RegisterOut)
async def register_new_team(team_creds: RegisterTeam, session: AsyncSession=Depends(get_session)):
    team = Team(name=team_creds.name, token=team_creds.token, stations=team_creds.stations)
    await team.save(session)
    return {"token": sign_jwt(team.id)}

@router.post("/login", summary="Login team", operation_id="login-team",
             description=login_team_description, response_model=RegisterOut)
async def login_team(team_creds: LoginInTeam, session: AsyncSession=Depends(get_session)):
    if team := await Team.get_team_by_token(team_creds.token, session):
        return {"token": sign_jwt(team.id)}
    return Response(status_code=404)

@router.get("/", summary="Get team info", operation_id="get-team-info",
            description=get_team_info_description, response_model=TeamInfo)
async def get_team_info(token: JWTHeader = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    if team := await Team.get_team_by_id(token.team_id, session):
        return TeamInfo.model_validate(team)
    return Response(status_code=404)