from db.database import Base
from sqlalchemy import Column,  Integer, String, DateTime, BigInteger

class PetsModel(Base):
    __tablename__ = "pet"
    id = Column(String, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    owner1 = Column(BigInteger, nullable=False)
    owner2 = Column(BigInteger, nullable=False)
    time_to_crack = Column(DateTime, nullable=False)
    essense = Column(String, nullable=False, default="egg")
    mood = Column(String, nullable=False, default="whole")
    