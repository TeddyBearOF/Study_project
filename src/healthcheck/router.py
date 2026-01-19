from fastapi import APIRouter

from typing import Dict


router = APIRouter()


@router.get('/api/v1/healthcheck', status_code=200)
async def healthcheck() -> Dict[str, str]:
    return {"status" : "ok"}
