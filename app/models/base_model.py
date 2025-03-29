from pydantic import BaseModel, Field
from typing import List, Dict


class Item(BaseModel):
    id: str
    name: str
    price: float


class AreaModel(BaseModel):
    AreaID: str
    UrgencyLevel: int = Field(ge=1, le=5)
    RequireResources: Dict[str, int]
    TimeConstrants: int


class TruckModel(BaseModel):
    TruckID: str
    AvailableResources: Dict[str, int]
    TravelTimeToArea: Dict[str, int]


class AssignmentModel(BaseModel):
    AreaID: str
    TruckID: str
    ResourcesDelivered: Dict[str, int]
