from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    number_of_comments = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
