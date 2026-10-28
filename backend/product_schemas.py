from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProductCategory = Literal[
    "Mutual Fund",
    "Fixed Deposit",
    "Government Bond",
    "Index Fund",
    "Other",
]

RiskLevel = Literal[
    "Low",
    "Moderate",
    "High",
]


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)

    category: ProductCategory

    description: str = Field(default="", max_length=2000)

    minimum_investment: float = Field(ge=0)

    # Illustrative annual percentage, not a guaranteed return.
    expected_annual_return: float = Field(ge=-100, le=100)

    risk_level: RiskLevel


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    category: ProductCategory | None = None
    description: str | None = Field(default=None, max_length=2000)
    minimum_investment: float | None = Field(default=None, ge=0)
    expected_annual_return: float | None = Field(default=None, ge=-100, le=100)
    risk_level: RiskLevel | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    minimum_investment: float
    expected_annual_return: float
    risk_level: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)