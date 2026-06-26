import random
import string
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import storage
from models import ShortnerRequest,ShortnerResponse,StatsResponse,UrlRecords

app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener with click tracking and link expiry",
    version="1.0.0"
)

BASE_URL = "http://localhost:8000"


def generate_short_code(length: int = 6) -> str:
    """Generating a random alphanumeric short code that isn't already taken"""
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(chars, k =length))
        if not storage.code_exists(code):
            return code
        

@app.post("/shorten", response_model = ShortnerResponse, status_code = 201)
def shorten_url(request: ShortnerRequest):
    """
    Shorten a URL. Optionally provide:
    - custom_code: your own short code (e.g. "my-link")
    - expiry_days: auto-expire the link after N days
    """

    if request.custom_code:
        if storage.code_exists(request.custom_code):
            raise HTTPException(
                status_code = 409,
                detail=f"Short code '{request.custom_code}' is already taken"

            )
        short_code = request.custom_code

    else:
        short_code = generate_short_code()
        
    #expiry calculation
    expires_on = None
    if request.expiry_days:
        expires_on = datetime.now() + timedelta(days=request.expiry_days)

    #Build and save the record
    record = UrlRecords(
        original_url = str(request.url),
        short_code = short_code,
        created_at = datetime.now(),
        expires_on = expires_on,
        click_count = 0,
    )
    storage.save_record(record)

    return ShortnerResponse(
        short_code=short_code,
        short_url=f"{BASE_URL}/{short_code}",
        original_url=str(request.url),
        expires_on = expires_on,
    )
    
@app.get("/{short_code}", status_code=307)
def redirect(short_code: str):
    record = storage.get_record(short_code)
    if not record:
        raise HTTPException(status_code=404, detail="Short code not found.")

    if storage.is_expired(record):
        storage.delete_record(short_code)
        raise HTTPException(status_code=410, detail="This link has expired.")

    storage.update_clicks(short_code)
    return RedirectResponse(url=record.original_url)
    
@app.delete("/{short_code}", status_code = 204)
def delete_url(short_code: str):
    """
    Delete a short URL by its code.
    Returns 204 No content on success.
    """

    deleted = storage.delete_record(short_code)
    if not deleted:
        raise HTTPException(status_code=404, detail = "Short code not found.")