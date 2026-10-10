from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer, Plan, Subscription
from app.schemas import (
    CustomerCreate, 
    CustomerResponse,
    PlanCreate, 
    PlanResponse,
    SubscriptionCreate,
    SubscriptionResponse
)

app = FastAPI(
    title="Banking Membership API",
    description="REST API for managing banking customers, membership plans, and subscriptions.",
    version="1.0.0",
)


@app.get("/health",tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.get("/customers", response_model=list[CustomerResponse], tags=["Customers"])
def get_customers(db: Session = Depends(get_db)):
    return db.scalars(select(Customer)).all()

@app.get("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

@app.post("/customers", response_model=CustomerResponse, status_code=201, tags=["Customers"])
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = Customer(
        name=customer_data.name,
        email=customer_data.email
    )

    db.add(new_customer)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Customer with this email already exists"
        )

    db.refresh(new_customer)

    return new_customer

@app.get("/plans", response_model=list[PlanResponse], tags=["Plans"])
def get_plans(db: Session = Depends(get_db)):
    return db.scalars(select(Plan)).all()

@app.post("/plans", response_model=PlanResponse, status_code=201, tags=["Plans"])
def create_plan(
    plan_data: PlanCreate,
    db: Session = Depends(get_db)
):
    new_plan = Plan(
        name=plan_data.name,
        monthly_price=plan_data.monthly_price
    )

    db.add(new_plan)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Plan with this name already exists"
        )

    db.refresh(new_plan)

    return new_plan

@app.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    status_code=201,
    tags=["Subscriptions"],
)
def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    # 1. Check whether the customer exists
    customer = db.get(Customer, subscription_data.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # 2. Check whether the plan exists
    plan = db.get(Plan, subscription_data.plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    # 3. Check whether the customer already has an active subscription
    existing_subscription = db.scalar(
        select(Subscription).where(
            Subscription.customer_id == subscription_data.customer_id,
            Subscription.status == "ACTIVE",
        )
    )

    if existing_subscription is not None:
        raise HTTPException(
            status_code=409,
            detail="Customer already has an active subscription",
        )

    # 4. Create the subscription
    new_subscription = Subscription(
        customer_id=subscription_data.customer_id,
        plan_id=subscription_data.plan_id,
        status="ACTIVE",
    )

    db.add(new_subscription)

    # 5. Save to PostgreSQL
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Subscription could not be created due to a database constraint",
        )

    db.refresh(new_subscription)

    return new_subscription