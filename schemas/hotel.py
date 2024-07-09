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
    images: List[Image]
    facilities: List[Facility]

class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    number_of_comments: int
    rating: float
    created_at: datetime
    images: List[Image]
    facilities: List[Facility]

    class Config:
        from_attributes = True
