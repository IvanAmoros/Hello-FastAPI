from sqlalchemy import Column, Integer, String, ForeignKey, Table, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database import Base

# Association table for the many-to-many relationship between Hotel and Facility
hotel_facility_association = Table(
    'hotel_facility_association', Base.metadata,
    Column('hotel_id', Integer, ForeignKey('hotels.id'), primary_key=True),
    Column('facility_id', Integer, ForeignKey('facilities.id'), primary_key=True)
)

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    number_of_comments = Column(Integer, nullable=False)
    rating = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    images = relationship("Image", back_populates="hotel")
    facilities = relationship("Facility", secondary=hotel_facility_association, back_populates="hotels")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)

    hotel = relationship("Hotel", back_populates="images")

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    hotels = relationship("Hotel", secondary=hotel_facility_association, back_populates="facilities")
