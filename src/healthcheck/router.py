from fastapi import APIRouter

from typing import Dict


router = APIRouter()


@router.get('/healthcheck', status_code=200)
async def healthcheck() -> Dict[str, str]:
    return {"status" : "ok"}
