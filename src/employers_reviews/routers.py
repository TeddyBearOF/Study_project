from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.employers_reviews.schemas import (
    EmployerCreate, EmployerResponse, EmployerUpdate,
)
from src.employers_reviews.services import EmployerService

router = APIRouter(prefix="/employers", tags=["employers"])


@router.post("/", response_model=EmployerResponse, status_code=status.HTTP_201_CREATED)
async def create_employer(
    employer_data: EmployerCreate,
    db: AsyncSession = Depends(get_session)
):
    return await EmployerService.create_employer(db, employer_data)


@router.get("/{employer_id}", response_model=EmployerResponse)
async def get_employer(
    employer_id: int,
    db: AsyncSession = Depends(get_session)
):
    employer = await EmployerService.get_employer_by_id(db, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


@router.put("/{employer_id}", response_model=EmployerResponse)
async def update_employer(
    employer_id: int,
    employer_data: EmployerUpdate,
    db: AsyncSession = Depends(get_session)
):
    employer = await EmployerService.get_employer_by_id(db, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return await EmployerService.update_employer(db, employer, employer_data)


@router.delete("/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employer(
    employer_id: int,
    db: AsyncSession = Depends(get_session)
):
    employer = await EmployerService.get_employer_by_id(db, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    await EmployerService.delete_employer(db, employer)