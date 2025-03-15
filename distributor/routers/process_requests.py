from typing import Literal, Dict

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel
from loguru import logger

from distributor.routers.redirect import Curator

router = APIRouter()

class Req(BaseModel):
    emb_name: str
    idx: Literal['tfidf', 'idea', 'combined', 'pure', 'delete']
    method: Literal['POST', 'GET', 'DELETE']
    content: Dict

@router.get("/redirect")
async def redirect_request(
        request: Request
):
    request_data = await request.json()
    ## та структура которая нужна описана в Req - тело передаваемое на эндпоинт может быть любым НО в очередь нужно поместить такое
    try:
        await Curator().put_event(request_data)
        return status.HTTP_200_OK
    except Exception as e:
        logger.error(f"there is an exception: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR

