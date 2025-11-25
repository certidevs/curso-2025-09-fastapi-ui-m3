from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ArtistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    birth_date: datetime | None