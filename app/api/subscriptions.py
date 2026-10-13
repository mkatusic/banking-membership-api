from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Customer, Plan, Subscription
from app.schemas import SubscriptionCreate, SubscriptionResponse


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.post("", response_model=SubscriptionResponse, status_code=201)
def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    # Verify that the customer exists
    customer = db.get(Customer, subscription_data.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # Verify that the plan exists
    plan = db.get(Plan, subscription_data.plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    # Check whether the customer already has an active subscription
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

    # Create the subscription
    new_subscription = Subscription(
        customer_id=subscription_data.customer_id,
        plan_id=subscription_data.plan_id,
        status="ACTIVE",
    )

    db.add(new_subscription)

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