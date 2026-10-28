from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class GoalCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)

    goal_type: Literal[
        "Education",
        "Retirement",
        "Home",
        "Vehicle",
        "Emergency Fund",
        "Travel",
        "Other",
    ]

    target_amount: float = Field(gt=0)
    current_savings: float = Field(ge=0)
    target_years: int = Field(ge=1, le=100)

    priority: Literal[
        "Low",
        "Medium",
        "High",
    ]


class GoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)

    goal_type: Literal[
        "Education",
        "Retirement",
        "Home",
        "Vehicle",
        "Emergency Fund",
        "Travel",
        "Other",
    ] | None = None

    target_amount: float | None = Field(default=None, gt=0)
    current_savings: float | None = Field(default=None, ge=0)
    target_years: int | None = Field(default=None, ge=1, le=100)

    priority: Literal[
        "Low",
        "Medium",
        "High",
    ] | None = None


class GoalResponse(BaseModel):
    id: int
    client_id: int
    title: str
    goal_type: str
    target_amount: float
    current_savings: float
    target_years: int
    priority: str

    model_config = ConfigDict(from_attributes=True)