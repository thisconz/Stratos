from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.db import get_db
from ...models.location import Location
from ..schemas.location import LocationCreate, LocationUpdate, LocationOut

router = APIRouter()

@router.get("/")
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    locations = result.scalars().all()
    return locations

@router.post("/")
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(**location.dict())
    db.add(new_location)
    db.commit()          # commit to save and generate fields
    db.refresh(new_location)  # refresh instance to get those generated fields
    return new_location

@router.put("/{id}", response_model=LocationOut)
def update_location(id: UUID, data: LocationUpdate, db: Session = Depends(get_db)):
    loc = db.query(Location).filter(Location.id == id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    loc.name = data.name
    db.commit()
    return loc

@router.delete("/{id}")
async def delete_location(id: UUID, db: AsyncSession = Depends(get_db)):
    # Query for the location
    result = await db.execute(select(Location).filter(Location.id == id))
    location = result.scalars().first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Delete and commit
    await db.delete(location)
    await db.commit()

    return {"detail": "Location deleted"}