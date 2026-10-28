
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


def utc_now():
    return datetime.now(timezone.utc)


# --------------------------------------------------
# 1. USERS
# --------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(30), nullable=False, default="relationship_manager")

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now)

    clients = relationship(
        "Client",
        back_populates="manager",
        cascade="all, delete-orphan",
    )


# --------------------------------------------------
# 2. CLIENTS
# --------------------------------------------------

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)

    email = Column(String(255), nullable=True)

    age = Column(Integer, nullable=True)

    annual_income = Column(Float, nullable=True)

    total_assets = Column(Float, nullable=True)

    risk_tolerance = Column(String(30), nullable=False, default="moderate")

    investment_experience = Column(String(30), nullable=True)

    notes = Column(Text, nullable=True)

    manager_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), default=utc_now)

    manager = relationship("User", back_populates="clients")

    financial_goals = relationship(
        "FinancialGoal",
        back_populates="client",
        cascade="all, delete-orphan",
    )

    simulations = relationship(
        "Simulation",
        back_populates="client",
        cascade="all, delete-orphan",
    )


# --------------------------------------------------
# 3. FINANCIAL GOALS
# --------------------------------------------------

class FinancialGoal(Base):
    __tablename__ = "financial_goals"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    title = Column(String(150), nullable=False)

    goal_type = Column(String(50), nullable=False)

    target_amount = Column(Float, nullable=False)

    current_savings = Column(Float, default=0.0, nullable=False)

    target_years = Column(Integer, nullable=False)

    priority = Column(String(30), default="medium", nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now)

    client = relationship(
        "Client",
        back_populates="financial_goals",
    )


# --------------------------------------------------
# 4. INVESTMENT PRODUCTS
# --------------------------------------------------

class InvestmentProduct(Base):
    __tablename__ = "investment_products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    category = Column(String(80), nullable=False)

    description = Column(Text, nullable=True)

    minimum_investment = Column(Float, nullable=False, default=0.0)

    expected_annual_return = Column(Float, nullable=True)

    risk_level = Column(String(30), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now)


# --------------------------------------------------
# 5. SIMULATIONS
# --------------------------------------------------

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    product_id = Column(
        Integer,
        ForeignKey("investment_products.id"),
        nullable=True,
    )

    initial_investment = Column(Float, nullable=False)

    monthly_contribution = Column(Float, nullable=False, default=0.0)

    investment_years = Column(Integer, nullable=False)

    assumptions = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now)

    client = relationship("Client", back_populates="simulations")

    product = relationship("InvestmentProduct")

    results = relationship(
        "SimulationResult",
        back_populates="simulation",
        cascade="all, delete-orphan",
    )


# --------------------------------------------------
# 6. SIMULATION RESULTS
# --------------------------------------------------

class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)

    simulation_id = Column(
        Integer,
        ForeignKey("simulations.id"),
        nullable=False,
        index=True,
    )

    scenario_name = Column(String(50), nullable=False)

    annual_return_assumption = Column(Float, nullable=False)

    projected_value = Column(Float, nullable=False)

    total_contributions = Column(Float, nullable=False)

    estimated_gain = Column(Float, nullable=False)

    explanatory_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now)

    simulation = relationship(
        "Simulation",
        back_populates="results",
    )
