from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Customer, Plan, Subscription
from app.schemas import SubscriptionCreate


class CustomerNotFoundError(Exception):
    pass


class PlanNotFoundError(Exception):
    pass


class ActiveSubscriptionExistsError(Exception):
    pass


class SubscriptionCreationError(Exception):
    pass


class SubscriptionNotFoundError(Exception):
    pass


class SubscriptionAlreadyCancelledError(Exception):
    pass



def create_subscription(
    db: Session,
    subscription_data: SubscriptionCreate,
) -> Subscription:

    # Check whether customer exists
    customer = db.get(Customer, subscription_data.customer_id)

    if customer is None:
        raise CustomerNotFoundError()

    # Check whether plan exists
    plan = db.get(Plan, subscription_data.plan_id)

    if plan is None:
        raise PlanNotFoundError()

    # Check whether customer already has an active subscription
    existing_subscription = db.scalar(
        select(Subscription).where(
            Subscription.customer_id == subscription_data.customer_id,
            Subscription.status == "ACTIVE",
        )
    )

    if existing_subscription is not None:
        raise ActiveSubscriptionExistsError()

    # Create new subscription
    new_subscription = Subscription(
        customer_id=subscription_data.customer_id,
        plan_id=subscription_data.plan_id,
        status="ACTIVE",
    )

    db.add(new_subscription)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        raise SubscriptionCreationError() from exc

    db.refresh(new_subscription)

    return new_subscription

def cancel_subscription(
    db: Session,
    subscription_id: int,
) -> Subscription:

    # Finds the subscription
    subscription = db.get(Subscription, subscription_id)

    # Checks whether it exists
    if subscription is None:
        raise SubscriptionNotFoundError()

    # Checks whether it is already cancelled
    if subscription.status == "CANCELLED":
        raise SubscriptionAlreadyCancelledError()

    # Updates the subscription
    subscription.status = "CANCELLED"
    subscription.cancelled_at = datetime.now(timezone.utc)

    # Saves the changes
    db.commit()

    # Refreshes the object
    db.refresh(subscription)

    return subscription