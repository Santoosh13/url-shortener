import random
import string
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db, engine
from keyvault import get_secret
from models import ShortnerRequest,ShortnerResponse,StatsResponse,Base,URLRecord

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener API backed by Azure PostgreSQL and key vault",
    version="2.0.0"
)

BASE_URL = get_secret("BASE-URL")


def generate_short_code(length: int = 6) -> str:
    """Generating a random alphanumeric short code that isn't already taken"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k =length))
        

@app.post("/shorten", response_model = ShortnerResponse, status_code = 201)
def shorten_url(request: ShortnerRequest,db:Session = Depends(get_db)):

    if request.custom_code:
        
        if request.custom_code:
            existing = db.query(URLRecord).filter(URLRecord.short_code == request.custom_code).first()
            if existing:
                raise HTTPException(status_code=409, detail=f"Short code '{request.custom_code}' is already taken.")
            short_code = request.custom_code
    else:
        short_code = generate_short_code()
        
    #expiry calculation
    expires_on = None
    
    if request.expiry_days:
        expires_on = datetime.now() + timedelta(days=request.expiry_days)

    record = URLRecord(
        short_code = short_code,
        original_url = str(request.url),
        created_at = datetime.now(),
        expires_on = expires_on,
        click_count = 0,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return ShortnerResponse(
        short_code=short_code,
        short_url=f"{BASE_URL}/{short_code}",
        original_url=str(request.url),
        expires_on = expires_on,
    )
    
@app.get("/{short_code}", status_code=307)
def redirect(short_code: str, db: Session = Depends(get_db)):
    """Redirect to the original URL."""

    record = db.query(URLRecord).filter(URLRecord.short_code == short_code).first()

    if not record:
        raise HTTPException(status_code=404, detail="Short code not found.")

    if record.expires_on and datetime.now() > record.expires_on:
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=410, detail="This link has expired.")

    record.click_count += 1
    db.commit()

    return RedirectResponse(url=record.original_url)
    
@app.get("/{short_code}/stats", response_model=StatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    """Get click stats for a short code."""
    record = db.query(URLRecord).filter(URLRecord.short_code == short_code).first()

    if not record:
        raise HTTPException(status_code = 404, detail = "Short code not found.")
    
    return record



@app.delete("/{short_code}", status_code = 204)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    """
    Delete a short URL by its code.
    Returns 204 No content on success.
    """

    record = db.query(URLRecord).filter(URLRecord.short_code == short_code).first()

    if not record:
        raise HTTPException(status_code = 404, detail = "Short code not found.")
    
    db.delete(record)
    db.commit()
