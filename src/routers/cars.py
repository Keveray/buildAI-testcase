from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional 
from sqlalchemy.orm import Session 
from src.schemas import UserCreate, UserUpdate, UserResponse, CarCreate, CarUpdate, CarResponse
from src.models import User, Car 
from src.database import get_db

router = APIRouter(prefix="/cars", tags=["cars"])

@router.post("/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    # Check if owner exists
    owner = db.query(User).filter(User.id == car.owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Владелец не найден")
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.get("/{car_id}", response_model=CarResponse)
def read_car(car_id: int, db: Session = Depends(get_db)): 
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return car

@router.get("/", response_model=List[CarResponse])
def read_cars(
    skip: int = 0, 
    limit: int = 100, 
    model: str = None, 
    year: int = None, 
    db: Session = Depends(get_db) 
):
    query = db.query(Car)
    if model:
        query = query.filter(Car.model.ilike(f"%{model}%"))
    if year:
        query = query.filter(Car.year == year)
    cars = query.offset(skip).limit(limit).all()
    return cars

@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car_update: CarUpdate, db: Session = Depends(get_db)): 
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Владлец не найден")
    if car_update.owner_id is not None:
        owner = db.query(User).filter(User.id == car_update.owner_id).first()
        if owner is None:
            raise HTTPException(status_code=404, detail="Владелец не найден")
    update_data = car_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)): 
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    db.delete(db_car)
    db.commit()
    return {"detail": "Машина удалена"}