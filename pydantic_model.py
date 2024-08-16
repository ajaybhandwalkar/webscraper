import uuid
from datetime import datetime, UTC
from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional


class TaskModel(PydanticBaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: str
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LegitimateSellerModel(PydanticBaseModel):
    id: int
    site: str
    ssp_domain_name: str
    publisher_id: str
    seller_relationship: str
    tag_id: str
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    run_id: str

    class Config:
        from_attributes = True


class StatsResponseModel(PydanticBaseModel):
    Average_Execution_Time: float
    message: Optional[list[str]] = None

    class Config:
        from_attributes = True
