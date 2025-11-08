from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IncidentCreate(BaseModel):
    text: str
    description: Optional[str] = None
    status: Optional[str] = "new"
    source: str

class IncidentUpdate(BaseModel):
    text: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None 
    source: Optional[str] = None

class IncidentResponse(BaseModel):
    id: int
    text: str
    description: Optional[str] = None
    status: str
    source: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserCreate):
    id: int
    created_at: datetime

class CarCreate(BaseModel):
    model: str
    year: int
    price_per_day: float
    owner_id: int

class CarUpdate(BaseModel):
    model: Optional[str] = None
    year: Optional[int] = None
    price_per_day: Optional[float] = None
    owner_id: Optional[int] = None

class CarResponse(CarCreate):
    id: int