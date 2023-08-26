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

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()