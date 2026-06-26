import json
import os
from datetime import datetime
from typing import Optional
from models import UrlRecords

DB_FILE = "urls.json"

def _load() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        content = f.read().strip()
        if not content:        # file exists but is empty
            return {}
        return json.loads(content)

def _save(data:dict):
    """Write all records to the json file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2,default=str)

def get_record(short_code: str) -> Optional[UrlRecords]:
    """Fetch a single URL record by its short code."""
    data = _load()
    if short_code not in data:
        return None
    return UrlRecords(**data[short_code])

def save_record(record: UrlRecords):
    """Save a new URL record."""
    data = _load()
    data[record.short_code] = record.model_dump()
    _save(data)

def update_clicks(short_code: str):
    """Increment the click counter for a short code"""
    data = _load()
    if short_code in data:
        data[short_code]["click_count"] += 1
        _save(data)


def delete_record(short_code: str)-> bool:
    """Delete a record. Returns True if it existed, False if not."""
    data = _load()
    if short_code not in data:
        return False
    del data[short_code]
    _save(data)
    return True

def code_exists(short_code: str) -> bool:
    """Check if a short code is already taken."""
    data = _load()
    return short_code in data

def is_expired(record: UrlRecords) -> bool:
    """Check if the url has passed its expiry date."""
    if record.expires_on is None:
        return False
    return datetime.now() > record.expires_on