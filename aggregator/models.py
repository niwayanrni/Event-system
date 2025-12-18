from pydantic import BaseModel

class Event(BaseModel):
    topic: str
    event_id: str
    timestamp: str
    source: str
    payload: dict
