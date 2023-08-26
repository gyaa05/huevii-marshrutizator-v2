from sqlalchemy import Column, Integer, String, select, update, ARRAY, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from models.db_session import SqlAlchemyBase as Base

class Team(Base):
    __tablename__="Teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    token = Column(String, nullable=False)
    stations = Column(ARRAY(Integer), nullable=False)
    cur_time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    all_time = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="free")
    cur_station = Column(Integer, nullable=False, default=0)

    @classmethod
    async def get_team_by_token(cls, token: str, session: AsyncSession):
        _ = await session.execute(select(cls).where(cls.token == token))
        return _.scalar()
    
    @classmethod
    async def get_team_by_id(cls, team_id: str, session: AsyncSession):
        _ = await session.execute(select(cls).where(cls.id == team_id))
        return _.scalar()
    
    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()