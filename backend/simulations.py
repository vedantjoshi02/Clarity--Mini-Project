from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db

from models import (
    Client,
    InvestmentProduct,
    Simulation,
    SimulationResult,
    User,
)

from simulation_schemas import (
    SimulationCreate,
    SimulationResponse,
    ScenarioResult,
)

from simulation_engine import calculate_scenarios


router = APIRouter(
    prefix="/simulations",
    tags=["Financial Simulations"],
)


@router.post(
    "/",
    response_model=SimulationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_simulation(
    simulation_data: SimulationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify that the client belongs to the logged-in manager.
    client = (
        db.query(Client)
        .filter(
            Client.id == simulation_data.client_id,
            Client.manager_id == current_user.id,
        )
        .first()
    )

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found.",
        )

    # If a product was selected, verify that it is active.
    if simulation_data.product_id is not None:
        product = (
            db.query(InvestmentProduct)
            .filter(
                InvestmentProduct.id == simulation_data.product_id,
                InvestmentProduct.is_active.is_(True),
            )
            .first()
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active investment product not found.",
            )

    results = calculate_scenarios(
        initial_investment=simulation_data.initial_investment,
        monthly_contribution=simulation_data.monthly_contribution,
        investment_years=simulation_data.investment_years,
    )

    simulation = Simulation(
        client_id=simulation_data.client_id,
        product_id=simulation_data.product_id,
        initial_investment=simulation_data.initial_investment,
        monthly_contribution=simulation_data.monthly_contribution,
        investment_years=simulation_data.investment_years,
        assumptions=(
            "Conservative: 4%, Moderate: 8%, Optimistic: 12%. "
            "Illustrative annual return assumptions; not forecasts."
        ),
    )

    db.add(simulation)
    db.flush()

    for result in results:
        db.add(
            SimulationResult(
                simulation_id=simulation.id,
                scenario_name=result["scenario_name"],
                annual_return_assumption=(
                    result["annual_return_assumption"]
                ),
                projected_value=result["projected_value"],
                total_contributions=result["total_contributions"],
                estimated_gain=result["estimated_gain"],
                explanatory_notes=result["explanatory_notes"],
            )
        )

    db.commit()
    db.refresh(simulation)

    return SimulationResponse(
        simulation_id=simulation.id,
        client_id=simulation.client_id,
        product_id=simulation.product_id,
        initial_investment=simulation.initial_investment,
        monthly_contribution=simulation.monthly_contribution,
        investment_years=simulation.investment_years,
        results=[
            ScenarioResult(
                scenario_name=result["scenario_name"],
                annual_return_assumption=(
                    result["annual_return_assumption"]
                ),
                projected_value=result["projected_value"],
                total_contributions=result["total_contributions"],
                estimated_gain=result["estimated_gain"],
                explanatory_notes=result["explanatory_notes"],
            )
            for result in results
        ],
    )


@router.get("/{simulation_id}")
def get_simulation(
    simulation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    simulation = (
        db.query(Simulation)
        .join(Client, Simulation.client_id == Client.id)
        .filter(
            Simulation.id == simulation_id,
            Client.manager_id == current_user.id,
        )
        .first()
    )

    if simulation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulation not found.",
        )

    return {
        "simulation_id": simulation.id,
        "client_id": simulation.client_id,
        "product_id": simulation.product_id,
        "initial_investment": simulation.initial_investment,
        "monthly_contribution": simulation.monthly_contribution,
        "investment_years": simulation.investment_years,
        "assumptions": simulation.assumptions,
        "results": [
            {
                "scenario_name": result.scenario_name,
                "annual_return_assumption": (
                    result.annual_return_assumption
                ),
                "projected_value": result.projected_value,
                "total_contributions": result.total_contributions,
                "estimated_gain": result.estimated_gain,
                "explanatory_notes": result.explanatory_notes,
            }
            for result in simulation.results
        ],
    }