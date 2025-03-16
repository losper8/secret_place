from typing import Literal, Dict, Optional

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, ValidationError
from loguru import logger

from distributor.routers.redirect import Curator

router = APIRouter()


class Req(BaseModel):
    emb_name: str
    idx: Literal['tfidf', 'idea', 'combined', 'pure', 'delete', 'read']
    method: Literal['POST', 'GET', 'DELETE']
    content: Optional[Dict]


@router.post("/redirect")
async def redirect_request(request: Request,
                           data: Req):
    try:
        result = await Curator().put_event(data)
        if result == 'err':
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        return result
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

