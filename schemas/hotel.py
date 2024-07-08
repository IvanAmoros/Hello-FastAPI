from pydantic import BaseModel

class HotelScrapeRequest(BaseModel):
    name: str

class HotelCreate(BaseModel):
    name: str
    location: str
    description: str
    number_of_comments: int

class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    number_of_comments: int
    created_at: str

    class Config:
        orm_mode = True
