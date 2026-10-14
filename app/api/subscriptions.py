from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import SubscriptionCreate, SubscriptionResponse
from app.services.subscription_service import (
    ActiveSubscriptionExistsError,
    CustomerNotFoundError,
    PlanNotFoundError,
    SubscriptionAlreadyCancelledError,
    SubscriptionCreationError,
    SubscriptionNotFoundError,
    cancel_subscription as cancel_subscription_service,
    create_subscription as create_subscription_service,
)


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=201,
)
def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_subscription_service(db, subscription_data)

    except CustomerNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    except PlanNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    except ActiveSubscriptionExistsError:
        raise HTTPException(
            status_code=409,
            detail="Customer already has an active subscription",
        )

    except SubscriptionCreationError:
        raise HTTPException(
            status_code=409,
            detail="Subscription could not be created due to a database constraint",
        )

@router.post(
    "/{subscription_id}/cancel",
    response_model=SubscriptionResponse,
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
):
    try:
        return cancel_subscription_service(db, subscription_id)

    except SubscriptionNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    except SubscriptionAlreadyCancelledError:
        raise HTTPException(
            status_code=409,
            detail="Subscription is already cancelled",
        )

