def calculate_projection(
    initial_investment: float,
    monthly_contribution: float,
    investment_years: int,
    annual_return: float,
) -> dict:
    """
    Calculate an illustrative investment projection.

    Contributions are assumed to be made at the end of each month.
    Returns are assumed to compound monthly.
    Taxes, fees, inflation, and volatility are excluded.
    """

    months = investment_years * 12
    monthly_rate = annual_return / 12

    total_contributions = (
        initial_investment
        + monthly_contribution * months
    )

    if monthly_rate == 0:
        projected_value = total_contributions
    else:
        initial_value = (
            initial_investment
            * (1 + monthly_rate) ** months
        )

        monthly_value = (
            monthly_contribution
            * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        )

        projected_value = initial_value + monthly_value

    estimated_gain = projected_value - total_contributions

    return {
        "projected_value": round(projected_value, 2),
        "total_contributions": round(total_contributions, 2),
        "estimated_gain": round(estimated_gain, 2),
    }


def calculate_scenarios(
    initial_investment: float,
    monthly_contribution: float,
    investment_years: int,
) -> list[dict]:

    scenarios = [
        {
            "scenario_name": "Conservative",
            "annual_return_assumption": 0.04,
        },
        {
            "scenario_name": "Moderate",
            "annual_return_assumption": 0.08,
        },
        {
            "scenario_name": "Optimistic",
            "annual_return_assumption": 0.12,
        },
    ]

    results = []

    for scenario in scenarios:
        projection = calculate_projection(
            initial_investment=initial_investment,
            monthly_contribution=monthly_contribution,
            investment_years=investment_years,
            annual_return=scenario["annual_return_assumption"] / 1,
        )

        results.append({
            "scenario_name": scenario["scenario_name"],
            "annual_return_assumption": (
                scenario["annual_return_assumption"] * 100
            ),
            **projection,
            "explanatory_notes": (
                "Illustrative mathematical projection only. "
                "Actual returns may differ significantly. "
                "Taxes, fees, inflation, and market volatility "
                "are not included."
            ),
        })

    return results