from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Plan
from app.schemas import PlanCreate, PlanResponse


router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.get("", response_model=list[PlanResponse])
def get_plans(db: Session = Depends(get_db)):
    return db.scalars(select(Plan)).all()


@router.post("", response_model=PlanResponse, status_code=201)
def create_plan(
    plan_data: PlanCreate,
    db: Session = Depends(get_db),
):
    new_plan = Plan(
        name=plan_data.name,
        monthly_price=plan_data.monthly_price,
    )

    db.add(new_plan)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Plan with this name already exists",
        )

    db.refresh(new_plan)

    return new_plan