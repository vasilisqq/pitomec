from db.database import Base
from sqlalchemy import Column,  Integer, String, DateTime, BigInteger, CheckConstraint, PrimaryKeyConstraint

class PetsModel(Base):
    __tablename__ = "pet"
    owner1 = Column(String,primary_key=True, nullable=False)
    owner2 = Column(String,primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    time_to_crack = Column(DateTime, nullable=False)
    time_to_hatch = Column(DateTime, nullable=True)
    time_to_unhappy = Column(DateTime, nullable=True)
    time_to_hungry = Column(DateTime, nullable=True)
    time_to_walk = Column(DateTime, nullable=True)
    essense = Column(String, nullable=False, default="egg")
    mood = Column(String, nullable=False, default="whole")