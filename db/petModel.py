from db.database import Base
from sqlalchemy import Column,  Integer, String, DateTime, BigInteger

class PetsModel(Base):
    __tablename__ = "pet"
    owner1 = Column(BigInteger,primary_key=True, nullable=False)
    owner2 = Column(BigInteger,primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    time_to_crack = Column(DateTime, nullable=False)
    essense = Column(String, nullable=False, default="egg")
    mood = Column(String, nullable=False, default="whole")
    