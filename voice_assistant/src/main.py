import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn.workers import UvicornWorker

from api.v1 import alice
from settings import config
from settings.logger import LOGGING

app = FastAPI(
    title=config.CommonSettings().project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(alice.router, prefix='/alice_api/v1', tags=['alice'])


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": LOGGING,
        "log_level": logging.DEBUG
    }
