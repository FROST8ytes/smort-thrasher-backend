from sqlmodel import SQLModel, Field, TIMESTAMP, text, Column
from typing import Optional
from datetime import datetime


class Record(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    time_stamp: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    trash_level: float | None = None
    image: str | None = None
