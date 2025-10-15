from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Device, Battery, DeviceBatteryLink
from app.database.base import engine, SessionLocal, Base
from app.schemas import DeviceCreate, DeviceOut, BatteryOut, BatteryCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/devices/", response_model=DeviceOut)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/devices/{device_id}", response_model=DeviceOut)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@app.post("/batteries/", response_model=BatteryOut)
def create_battery(battery: BatteryCreate, db: Session = Depends(get_db)):
    db_battery = Battery(**battery.dict())
    db.add(db_battery)
    db.commit()
    db.refresh(db_battery)
    return db_battery

@app.post("/devices/{device_id}/batteries/{battery_id}")
def add_battery_to_device(device_id: int, battery_id: int, db: Session = Depends(get_db)):
    count = db.query(DeviceBatteryLink).filter(DeviceBatteryLink.device_id == device_id).count()
    if count >= 5:
        raise HTTPException(status_code=400, detail="Maximum 5 batteries per device")

    battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    link = DeviceBatteryLink(device_id=device_id, battery_id=battery_id)
    db.add(link)
    db.commit()
    return {"message": "Battery added to device"}