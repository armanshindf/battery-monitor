from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    firmware_version = Column(String(50), nullable=False)
    status = Column(Boolean, default=False)

    batteries = relationship("Battery", secondary="device_battery_link", back_populates="device")

class Battery(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    nominal_voltage = Column(Float, nullable=False)
    remaining_capacity = Column(Float, nullable=False)
    lifespan = Column(Date, nullable=False)

    device = relationship("Device", secondary="device_battery_link", back_populates="batteries")

class DeviceBatteryLink(Base):
    __tablename__ = "device_battery_link"

    device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"), primary_key=True)