from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.scalars(select(Customer)).all()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
):
    new_customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
    )

    db.add(new_customer)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Customer with this email already exists",
        )

    db.refresh(new_customer)

    return new_customer