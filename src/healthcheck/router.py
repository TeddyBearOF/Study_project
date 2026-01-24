from fastapi import APIRouter

from typing import Dict

from src.healthcheck.schemas import HealthCheckResponse

router = APIRouter()


@router.get('/healthcheck', status_code=200)
async def healthcheck() -> HealthCheckResponse:
    return HealthCheckResponse(status="OK")
