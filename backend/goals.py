from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Client, FinancialGoal, User

from goal_schemas import (
    GoalCreate,
    GoalUpdate,
    GoalResponse,
)

router = APIRouter(
    prefix="/clients",
    tags=["Financial Goals"],
)


def get_managed_client(
    client_id: int,
    db: Session,
    current_user: User,
):
    client = (
        db.query(Client)
        .filter(
            Client.id == client_id,
            Client.manager_id == current_user.id,
        )
        .first()
    )

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found.",
        )

    return client


@router.post(
    "/{client_id}/goals",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_goal(
    client_id: int,
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_managed_client(client_id, db, current_user)

    goal = FinancialGoal(
        client_id=client_id,
        title=goal_data.title,
        goal_type=goal_data.goal_type,
        target_amount=goal_data.target_amount,
        current_savings=goal_data.current_savings,
        target_years=goal_data.target_years,
        priority=goal_data.priority,
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


@router.get(
    "/{client_id}/goals",
    response_model=list[GoalResponse],
)
def get_client_goals(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_managed_client(client_id, db, current_user)

    return (
        db.query(FinancialGoal)
        .filter(FinancialGoal.client_id == client_id)
        .order_by(FinancialGoal.id.desc())
        .all()
    )


@router.patch(
    "/{client_id}/goals/{goal_id}",
    response_model=GoalResponse,
)
def update_goal(
    client_id: int,
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_managed_client(client_id, db, current_user)

    goal = (
        db.query(FinancialGoal)
        .filter(
            FinancialGoal.id == goal_id,
            FinancialGoal.client_id == client_id,
        )
        .first()
    )

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial goal not found.",
        )

    updates = goal_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    return goal


@router.delete(
    "/{client_id}/goals/{goal_id}",
)
def delete_goal(
    client_id: int,
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_managed_client(client_id, db, current_user)

    goal = (
        db.query(FinancialGoal)
        .filter(
            FinancialGoal.id == goal_id,
            FinancialGoal.client_id == client_id,
        )
        .first()
    )

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial goal not found.",
        )

    db.delete(goal)
    db.commit()

    return {
        "message": "Financial goal deleted successfully."
    }