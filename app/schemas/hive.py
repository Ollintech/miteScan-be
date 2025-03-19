from pydantic import BaseModel, Optional
from sqlalchemy import UniqueConstraint

class HiveCreate(BaseModel):
    user_id: int
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
    user_id: int
    bee_type_id: int
    location_lat: float
    location_lng: float
    size: int
    humidity: Optional[float] = None
    temperature: Optional[float] = None

    class Config:
        orm_mode = True

class HiveUpdate(BaseModel):
    user_id: Optional[int] = None
    bee_type_id: Optional[int] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    size: Optional[int] = None
    humidity: Optional[float] = None
    temperature: Optional[float] = None
