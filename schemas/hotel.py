from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Image(BaseModel):
    url: str

    class Config:
        from_attributes = True

class Facility(BaseModel):
    name: str

    class Config:
        from_attributes = True

class HotelScrapeRequest(BaseModel):
    name: str

class HotelCreate(BaseModel):
    name: str
    location: str
    description: str
    number_of_comments: int
    rating: float
    hotel_url: str
    images: List[Image]
    facilities: List[Facility]

class HotelUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    description: Optional[str]
    number_of_comments: Optional[int]
    rating: Optional[float]
    hotel_url: Optional[str]
    images: Optional[List[Image]]
    facilities: Optional[List[Facility]]

class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    number_of_comments: int
    rating: float
    created_at: datetime
    hotel_url: str
    images: List[Image]
    facilities: List[Facility]

    class Config:
        from_attributes = True
