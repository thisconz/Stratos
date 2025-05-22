from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.db import get_db
from ...models.location import Location
from ..schemas.location import LocationCreate, LocationUpdate, LocationOut
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LocationOut])
async def get_locations(
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = await db.execute(select(Location))
    locations = result.scalars().all()
    return locations

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_location = Location(**location.dict())
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location

@router.put("/{id}", response_model=LocationOut)
async def update_location(
    id: UUID,
    data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = await db.execute(select(Location).filter(Location.id == id))
    loc = result.scalars().first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    loc.name = data.name
    await db.commit()
    await db.refresh(loc)
    return loc

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Query for the location
    result = await db.execute(select(Location).filter(Location.id == id))
    location = result.scalars().first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Delete and commit
    await db.delete(location)
    await db.commit()

    return