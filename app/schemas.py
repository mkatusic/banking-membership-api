from pydantic import BaseModel, ConfigDict, EmailStr, Field
from decimal import Decimal
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr

class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    monthly_price: Decimal

class PlanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    monthly_price: Decimal = Field(ge=0, decimal_places=2)

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