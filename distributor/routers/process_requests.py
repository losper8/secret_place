from typing import Literal, Dict, Optional, List, Union

from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from loguru import logger

from distributor.routers.redirect import Curator

router = APIRouter()


class Req(BaseModel):
    emb_name: str
    idx: Literal['search_tfidf', 'add_idea', 'search_embeddings', 'search_combined', 'delete', 'train_tfidf', 'embeddings_size', 'first_time_load_embeddings', 'read']
    method: Literal['POST', 'GET', 'DELETE']
    content: Optional[Union[Dict, List[Dict]]]


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

