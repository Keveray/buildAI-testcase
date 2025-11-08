from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session 
from src.schemas import IncidentCreate, IncidentUpdate, IncidentResponse 
from src.models import Incident
from src.database import get_db

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=IncidentResponse)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    db_incident = Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/", response_model=List[IncidentResponse])
def read_incidents(
    status: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    
    incidents = query.offset(skip).limit(limit).all()
    return incidents

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident_status(incident_id: int, status_update: str, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Инциндент не найден")
        
    db_incident.status = status_update
    db.commit()
    db.refresh(db_incident)
    return db_incident