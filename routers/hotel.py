from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.hotel import HotelCreate, HotelResponse
from crud.hotel import create_hotel, get_hotels, get_hotel
from database import get_db

router = APIRouter()

@router.post("/hotels/", response_model=HotelResponse)
def create_hotel_view(hotel: HotelCreate, db: Session = Depends(get_db)):
    return create_hotel(db=db, hotel=hotel)

@router.get("/hotels/", response_model=List[HotelResponse])
def read_hotels(db: Session = Depends(get_db)):
    return get_hotels(db=db)

@router.get("/hotels/{hotel_id}", response_model=HotelResponse)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = get_hotel(db=db, hotel_id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel
