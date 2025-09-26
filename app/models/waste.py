from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Waste(Base):
    __tablename__ = "waste"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    quantity_kg = Column(Float)
    collected_at = Column(Date)
