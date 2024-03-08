import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from settings.logger import LOGGING

logging_config.dictConfig(LOGGING)


class CommonSettings(BaseSettings):
    project_name: str = 'voice_assistent'
    cinema_api_url: str = 'http://nginx/api/v1'
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
