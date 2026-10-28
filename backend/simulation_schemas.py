from pydantic import BaseModel, Field


class SimulationCreate(BaseModel):
    client_id: int = Field(gt=0)

    product_id: int | None = Field(default=None, gt=0)

    initial_investment: float = Field(ge=0)

    monthly_contribution: float = Field(ge=0)

    investment_years: int = Field(ge=1, le=100)


class ScenarioResult(BaseModel):
    scenario_name: str
    annual_return_assumption: float
    projected_value: float
    total_contributions: float
    estimated_gain: float
    explanatory_notes: str


class SimulationResponse(BaseModel):
    simulation_id: int
    client_id: int
    product_id: int | None
    initial_investment: float
    monthly_contribution: float
    investment_years: int
    results: list[ScenarioResult]