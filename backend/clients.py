from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Client, User
from client_schemas import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_client = (
        db.query(Client)
        .filter(
            Client.manager_id == current_user.id,
            Client.email == str(client_data.email),
        )
        .first()
    )

    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A client with this email already exists in your account.",
        )

    client = Client(
        full_name=client_data.full_name,
        email=str(client_data.email),
        age=client_data.age,
        annual_income=client_data.annual_income,
        total_assets=client_data.total_assets,
        risk_tolerance=client_data.risk_tolerance,
        investment_experience=client_data.investment_experience,
        notes=client_data.notes,
        manager_id=current_user.id,
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.get("/", response_model=list[ClientResponse])
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Client)
        .filter(Client.manager_id == current_user.id)
        .order_by(Client.id.desc())
        .all()
    )


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    updates = client_data.model_dump(exclude_unset=True)

    if "email" in updates and updates["email"] is not None:
        updates["email"] = str(updates["email"])

        duplicate = (
            db.query(Client)
            .filter(
                Client.manager_id == current_user.id,
                Client.email == updates["email"],
                Client.id != client.id,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another client already uses this email.",
            )

    for field, value in updates.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client


@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    db.delete(client)
    db.commit()

    return {"message": "Client deleted successfully."}