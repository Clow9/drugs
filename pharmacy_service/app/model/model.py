from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class Drug(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    name: str
    manufacturer: str
    expiration_date: datetime
    description: Optional[str] = None
