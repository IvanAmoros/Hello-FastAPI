from sqlalchemy.orm import Session
from models.hotel import Hotel
from schemas.hotel import HotelCreate

def create_hotel(db: Session, hotel: HotelCreate):
    db_hotel = Hotel(**hotel.model_dump())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotels(db: Session):
    return db.query(Hotel).all()

def get_hotel(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()
