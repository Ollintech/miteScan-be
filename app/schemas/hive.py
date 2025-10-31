from pydantic import BaseModel
from typing import Optional
from sqlalchemy import UniqueConstraint

class HiveCreate(BaseModel):
    account: str
    bee_type_id: int
    location_lat: float
    location_lng: float
    size: int
    humidity: Optional[float] = None
    temperature: Optional[float] = None

    __table_args__ = (
        UniqueConstraint('location_lat', 'location_lng', name='unique_hive_location'),
    )

class HiveResponse(BaseModel):
    id: int
    account: str
    bee_type_id: int
    location_lat: float
    location_lng: float
    size: int
    humidity: Optional[float] = None
    temperature: Optional[float] = None

    class Config:
        from_attributes = True

class HiveUpdate(BaseModel):
    account: Optional[str] = None
    bee_type_id: Optional[int] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    size: Optional[int] = None
    humidity: Optional[float] = None
    temperature: Optional[float] = None
