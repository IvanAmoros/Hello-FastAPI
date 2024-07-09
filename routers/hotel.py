from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.hotel import HotelScrapeRequest, HotelCreate, HotelResponse, Image, Facility
from crud.hotel import create_hotel, get_hotels, get_hotel, get_hotel_by_name
from database import get_db
from scraper import scrape_hotel_details

router = APIRouter()

@router.post("/hotels/scrape", response_model=HotelResponse)
def scrape_and_create_hotel(hotel_request: HotelScrapeRequest, db: Session = Depends(get_db)):
    try:
        hotel_details = scrape_hotel_details(hotel_request.name)
        
        # Prepare image and facility data
        images = [Image(url=url) for url in hotel_details['images']]
        facilities = [Facility(name=name) for name in hotel_details['facilities']]
        
        hotel_create_data = HotelCreate(
            name=hotel_details['name'],
            location=hotel_details['location'],
            description=hotel_details['description'],
            number_of_comments=hotel_details['number_of_comments'],
            rating=hotel_details['rating'],
            images=images,
            facilities=facilities
        )
        db_hotel = create_hotel(db=db, hotel=hotel_create_data)
        return db_hotel
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

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
