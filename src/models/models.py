from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime 

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    price_per_day = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

class Incident(Base):
    __tablename__ = "incidents" 
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    description = Column(String, nullable=True)
    status = Column(String, default="new") 
    source = Column(String) 
    created_at = Column(DateTime, default=datetime.utcnow)
