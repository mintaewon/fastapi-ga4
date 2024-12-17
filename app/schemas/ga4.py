from typing import List, Dict, Any
from pydantic import BaseModel

class GA4RequestSchema(BaseModel):
    property_id: str
    start_date: str
    end_date: str
    metrics_list: List[str]
    dimensions_list: List[str]
    limit: int = 100000  # default value
    offset: int = 0  # default value

class GA4ResponseSchema(BaseModel):
    status: str
    data: List[dict]
