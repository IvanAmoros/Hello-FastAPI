from sqlalchemy.orm import Session
from models.hotel import Hotel, Image, Facility
from schemas.hotel import HotelCreate

def get_hotel_by_name(db: Session, name: str):
    return db.query(Hotel).filter(Hotel.name == name).first()

def get_facility_by_name(db: Session, name: str):
    return db.query(Facility).filter(Facility.name == name).first()

def create_hotel(db: Session, hotel: HotelCreate):
    # Check if hotel already exists
    existing_hotel = get_hotel_by_name(db, hotel.name)
    if existing_hotel:
        return existing_hotel

    db_hotel = Hotel(
        name=hotel.name,
        location=hotel.location,
        description=hotel.description,
        number_of_comments=hotel.number_of_comments,
        rating=hotel.rating,
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)

    # Save images
    for image in hotel.images:
        db_image = Image(url=image.url, hotel_id=db_hotel.id)
        db.add(db_image)

    # Save facilities
    for facility in hotel.facilities:
        existing_facility = get_facility_by_name(db, facility.name)
        if existing_facility:
            db_hotel.facilities.append(existing_facility)
        else:
            db_facility = Facility(name=facility.name)
            db.add(db_facility)
            db_hotel.facilities.append(db_facility)

    db.commit()
    return db_hotel

def get_hotels(db: Session):
    return db.query(Hotel).all()

def get_hotel(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()
