from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


Base = declarative_base()

class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(Integer)
    space_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("space_type.id"))
    space_type: Mapped["SpaceTypes"] = relationship("SpaceTypes", back_populates="logs")
    event_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("event_type.id"))
    event_type: Mapped["EventTypes"] = relationship("EventTypes", back_populates="logs")


class SpaceTypes(Base):
    __tablename__ = "space_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    logs: Mapped[list["Logs"]] = relationship("Logs", back_populates="space_type")


class EventTypes(Base):
    __tablename__ = "event_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    logs: Mapped[list["Logs"]] = relationship("Logs", back_populates="event_type")