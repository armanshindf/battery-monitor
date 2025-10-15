from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class BatteryCreate(BaseModel):
    name: str
    nominal_voltage: float
    remaining_capacity: float
    lifespan: date

class BatteryOut(BatteryCreate):
    id: int

    class Config:
        orm_mode = True

class DeviceCreate(BaseModel):
    name: str
    firmware_version: str
    status: bool = False

class DeviceOut(DeviceCreate):
    id: int
    batteries: List[BatteryOut] = []
    class Config:
        orm_mode = True
