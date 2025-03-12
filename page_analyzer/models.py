from dataclasses import dataclass
from datetime import datetime


@dataclass
class Site:
    """
    Site dataclass
    """
    id: int = None
    url: str
    created_at: datetime = None


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
    created_at: datetime = None
