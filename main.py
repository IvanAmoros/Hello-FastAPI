from fastapi import FastAPI

from database import engine, Base
from routers import hotel

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(hotel.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Scraper API!"}