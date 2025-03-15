import argparse
import asyncio
import sys

import uvicorn

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from distributor.config.pydantic_models import Config
from distributor.routers.redirect import Curator
from distributor.routers import process_requests

ApplicationName = "Distributor service"


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def start_app():
    parser = argparse.ArgumentParser(description=ApplicationName)
    parser.add_argument(
        "-c",
        "--config",
        nargs="?",
        dest="config",
        required=True,
        help="Path to configuration file"
    )
    args = parser.parse_args()
    config = Config(args.config)

    api_conf = config.api

    output = config.log.output_file if config.log.output_file else sys.stderr
    logger.add(output, format="{time} {level} {message}", level=config.log.level)

    app = FastAPI(
        debug=True,
        title='Distributor',
    )

    configure_cors(app)

    queue = asyncio.Queue()
    curator = Curator(queue=queue, embs_cfg=config.containers)

    app.include_router(process_requests.router, prefix="/api/v1")

    @app.get("/", include_in_schema=False)
    async def redirect_from_root() -> RedirectResponse:
        return RedirectResponse(url='/docs')

    @app.on_event("startup")
    async def startup():
        await Curator().process_queue()

    uvicorn.run(app, host=api_conf.host, port=api_conf.port)