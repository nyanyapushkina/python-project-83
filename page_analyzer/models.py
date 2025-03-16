from dataclasses import dataclass
from datetime import datetime


@dataclass
class Site:
    """
    Site dataclass
    """
    url: str
    id: int = None
    created_at: datetime = None
    last_check: datetime = None
    status_code: int = None 


@dataclass
class UrlCheck:
    """
    Check dataclass
    """
    url_id: int
    status_code: int
    h1: str
    title: str
    description: str
    id: int = None
    created_at: datetime = None
