from pathlib import Path
from typing import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict

# /**/7_patres/
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseCustomSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / '.env.public',
            BASE_DIR / '.env',
        ),
        case_sensitive=False,
        extra='allow',
        env_prefix='',
        env_nested_delimiter='',
    )

    @classmethod
    def set_app_name_as_source(cls, app_names: Sequence[str]):

        env_files = list(cls.model_config["env_file"])

        for app_name in app_names:
            env_files.append(BASE_DIR / f'{app_name}/.env.public')
            env_files.append(BASE_DIR / f'{app_name}/.env')

        cls.model_config["env_file"] = (
            *env_files,
        )