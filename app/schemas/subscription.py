from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubscriptionCreate(BaseModel):
    customer_id: int = Field(gt=0)
    plan_id: int = Field(gt=0)


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    plan_id: int
    status: str
    created_at: datetime