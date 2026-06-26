from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ShortnerRequest(BaseModel):
    url : HttpUrl
    custom_code : Optional[str] = None
    expiry_days : Optional[int] = None


class UrlRecords(BaseModel):
    original_url : str
    short_code : str
    created_at : datetime
    expires_on : Optional[datetime]
    click_count : int = 0

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