from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# ---------- SQLALchemy Base----------------------------------

class Base(DeclarativeBase):
    pass

# ----------- Datbase Model (what gets stored in PostgreSQL)---

class URLRecord(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True,index = True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default = datetime.now)
    expires_on = Column(DateTime, nullable = True)
    click_count = Column(Integer, default = 0)


# --------Pydantic Models (request/response validation)

class ShortnerRequest(BaseModel):
    url : HttpUrl
    custom_code : Optional[str] = None
    expiry_days : Optional[int] = None


class ShortnerResponse(BaseModel):
    short_code : str
    short_url : str
    original_url : str
    expires_on : Optional[datetime] = None

class StatsResponse(BaseModel):
    short_code : str
    original_url : str
    click_count : int
    created_at : datetime
    expires_on : Optional[datetime] = None