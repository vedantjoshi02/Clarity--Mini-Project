from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    age: int = Field(ge=18, le=120)
    annual_income: float = Field(ge=0)
    total_assets: float = Field(ge=0)

    risk_tolerance: Literal[
        "Conservative",
        "Moderate",
        "Aggressive"
    ]

    investment_experience: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    notes: str | None = Field(default=None, max_length=2000)


class ClientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=120)
    annual_income: float | None = Field(default=None, ge=0)
    total_assets: float | None = Field(default=None, ge=0)

    risk_tolerance: Literal[
        "Conservative",
        "Moderate",
        "Aggressive"
    ] | None = None

    investment_experience: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ] | None = None

    notes: str | None = Field(default=None, max_length=2000)


class ClientResponse(BaseModel):
    id: int
    full_name: str
    email: str
    age: int
    annual_income: float
    total_assets: float
    risk_tolerance: str
    investment_experience: str
    notes: str | None

    model_config = ConfigDict(from_attributes=True)