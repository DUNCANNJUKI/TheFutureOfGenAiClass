from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.waste import Waste
from datetime import date
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/waste",
    tags=["Waste Management"]
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class WasteCreate(BaseModel):
    type: str
    quantity_kg: float
    collected_at: date

class WasteOut(WasteCreate):
    id: int
    class Config:
        orm_mode = True

# POST: Create new record
@router.post("/", response_model=WasteOut)
def create_waste(waste: WasteCreate, db: Session = Depends(get_db)):
    db_waste = Waste(**waste.dict())
    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)
    return db_waste

# GET: All records
@router.get("/", response_model=List[WasteOut])
def get_all_waste(db: Session = Depends(get_db)):
    return db.query(Waste).all()

# GET: Record by ID
@router.get("/{waste_id}", response_model=WasteOut)
def get_waste(waste_id: int, db: Session = Depends(get_db)):
    waste = db.query(Waste).filter(Waste.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste record not found")
    return waste

# DELETE: Record by ID
@router.delete("/{waste_id}")
def delete_waste(waste_id: int, db: Session = Depends(get_db)):
    waste = db.query(Waste).filter(Waste.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste record not found")
    db.delete(waste)
    db.commit()
    return {"message": f"Waste record {waste_id} deleted"}
