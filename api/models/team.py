import math
from sqlalchemy import Column, Integer, String, select, update, ARRAY, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from models.station import Station

from models.db_session import SqlAlchemyBase as Base

class Team(Base):
    __tablename__="Teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    token = Column(String, nullable=False)
    stations = Column(ARRAY(Integer), nullable=False)
    cur_time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    all_time = Column(Integer, nullable=False, default=0)
    cur_station = Column(Integer, nullable=False, default=0)

    @classmethod
    async def get_team_by_token(cls, token: str, session: AsyncSession):
        _ = await session.execute(select(cls).where(cls.token == token))
        return _.scalar()
    
    @classmethod
    async def get_team_by_id(cls, team_id: int, session: AsyncSession):
        _ = await session.execute(select(cls).where(cls.id == team_id))
        return _.scalar()
    
    @classmethod
    async def get_next_station(cls, team_id: int, session: AsyncSession):
        if team := await session.execute(select(cls).where(cls.id==team_id)):
            team = team.scalar()
            start_lat = 0
            start_long = 0
            if team.cur_station != 0:
                station = await Station.get_station_by_id(team.cur_station, session)
                start_lat, start_long = station.latitude, station.longtitude
            check_stations = []
            for _, station_id in enumerate(team.stations):
                if station_id == team.cur_station:
                    continue
                station = await Station.get_station_by_id(station_id, session)
                length = math.sqrt((start_lat-station.latitude)**2 + (start_long-station.longtitude)**2)
                check_stations.append([station_id, length])
            check_stations = sorted(check_stations, key=lambda x: x[1])
            for station in check_stations:
                if await Station.get_status(station[0], session) == "free":
                    await Station.freeze_station(station[0], session)
                    team.cur_station = station[0]
                    team.cur_time = datetime.datetime.now()
                    team.stations.remove(team.cur_station)
                    await session.execute(update(cls).where(cls.id == team.id).values(stations = team.stations))
                    await session.commit()
                    return await Station.get_station_by_id(station[0], session)
        return None
        
    @classmethod
    async def complete_station(cls, team_id: int, flag: str, session: AsyncSession):
        if team := await session.execute(select(cls).where(cls.id == team_id)):
            team = team.scalar()
            if await Station.check_flag(team.cur_station, flag, session):
                await Station.unfreeze_station(team.cur_station, session)
                team.all_time = team.all_time + (datetime.datetime.now() - team.cur_time).total_seconds()
                await session.commit()
                if len(team.stations) == 0:
                    return 1
                return 2
        return 3
    
    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()