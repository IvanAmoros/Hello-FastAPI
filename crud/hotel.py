from sqlalchemy.orm import Session
from models.hotel import Hotel, Image, Facility
from schemas.hotel import HotelCreate, HotelUpdate


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
        hotel_url=hotel.hotel_url,
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

def get_hotel_by_id(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()

def get_hotel_by_name(db: Session, name: str):
    return db.query(Hotel).filter(Hotel.name == name).first()

def update_hotel(db: Session, hotel_id: int, hotel_update: HotelUpdate):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if db_hotel is None:
        return None

    # Update hotel attributes
    for key, value in hotel_update.dict(exclude_unset=True).items():
        if key == 'images':
            # Clear existing images and add new ones
            db.query(Image).filter(Image.hotel_id == hotel_id).delete()
            db_hotel.images = [Image(url=img['url'], hotel_id=hotel_id) for img in value]
        elif key == 'facilities':
            # Clear existing facilities and add new ones
            db_hotel.facilities = []
            for fac in value:
                existing_facility = get_facility_by_name(db, fac['name'])
                if existing_facility:
                    db_hotel.facilities.append(existing_facility)
                else:
                    new_facility = Facility(name=fac['name'])
                    db.add(new_facility)
                    db_hotel.facilities.append(new_facility)
        else:
            setattr(db_hotel, key, value)

    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if db_hotel is None:
        return None

    # Delete associated images
    db_images = db.query(Image).filter(Image.hotel_id == hotel_id).all()
    for db_image in db_images:
        db.delete(db_image)
    
    # Delete associated facilities
    db_hotel.facilities.clear()
    
    # Delete the hotel
    db.delete(db_hotel)
    db.commit()
    return db_hotel
