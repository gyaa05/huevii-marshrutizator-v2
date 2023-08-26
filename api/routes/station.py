from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from descriptions.station import *
from pydantic_models.station import CreateStation, GetStation
from models.db_session import get_session
from models.station import Station
from auth.auth_bearer import JWTBearer, JWTHeader

router = APIRouter()

@router.post("/create", summary="Create station", operation_id="create-station",
             description=create_station_description, response_class=Response)
async def create_station(station_creds: CreateStation, session: AsyncSession = Depends(get_session)):
    station = Station(name=station_creds.name, description=station_creds.description, latitude=station_creds.latitude, longtitude=station_creds.longtitude, flag=station_creds.flag)
    await station.save(session)
    return Response(status_code=202)

@router.get("/{station_id}", summary="Get station by id", operation_id="get-station-by-id",
            description=get_station_by_id_description, dependencies=[Depends(JWTBearer())])
async def get_station_by_id(station_id: int, session: AsyncSession = Depends(get_session)):
    if station := await Station.get_station_by_id(station_id, session):
        return GetStation.model_validate(station)
    return Response(status_code=404)