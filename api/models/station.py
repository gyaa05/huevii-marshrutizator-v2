from sqlalchemy import Column, Integer, String, select, update, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base

class Station(Base):
    __tablename__="Stations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="free")
    latitude = Column(Numeric(12, 10), nullable=False)
    longtitude = Column(Numeric(12, 10), nullable=False)
    flag = Column(String, nullable=False)

    @classmethod
    async def get_station_by_id(cls, station_id: int, session: AsyncSession):
        _ = await session.execute(select(cls).where(cls.id == station_id))
        return _.scalar()
    
    @classmethod
    async def freeze_station(cls, station_id: int, session: AsyncSession):
        await session.execute(update(cls).where(cls.id==station_id).values(status="busy"))
        await session.commit()

    @classmethod
    async def unfreeze_station(cls, station_id: int, session: AsyncSession):
        await session.execute(update(cls).where(cls.id==station_id).values(status="free"))  
        await session.commit()  

    @classmethod
    async def check_flag(cls, station_id: int, flag: str, session: AsyncSession):
        if station := await session.execute(select(cls).where(cls.id == station_id)):
            return flag == station.scalar().flag
        return False
    
    @classmethod
    async def get_status(cls, station_id: int, session: AsyncSession):
        if station := await session.execute(select(cls).where(cls.id == station_id)):
            return station.scalar().status
    
    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()