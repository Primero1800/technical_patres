import logging
from pathlib import Path
from typing import Literal

from src.tools import BaseCustomSettings


# /**7_patres/src
BASE_DIR = Path(__file__).resolve().parent.parent


class CustomSettings(BaseCustomSettings):
    pass


CustomSettings.set_app_name_as_source(
    ('src',)
)


class AppSettings(CustomSettings):
    APP_BASE_DIR: str = str(BASE_DIR)
    APP_NAME: str
    APP_TITLE: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    API_PREFIX: str
    API_V1_PREFIX: str


class AppRunConfig(CustomSettings):
    APP_PATH: str
    APP_HOST: str
    APP_PORT: int
    APP_RELOAD: bool


class Auth(CustomSettings):
    AUTH_TOKEN_LIFETIME: int

    AUTH_PRIVATE_KEY: Path = BASE_DIR / "core" / "certs" / "jwt-private.pem"
    AUTH_PUBLIC_KEY: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"

    # AUTH_RESET_PASSWORD_TOKEN_SECRET: str
    # AUTH_VERIFICATION_TOKEN_SECRET: str

    # AUTH_VERIFICATION_TOKEN_LIFETIME_SECONDS: int
    # AUTH_RESET_PASSWORD_TOKEN_LIFETIME_SECONDS: int


class DB(CustomSettings):

    DB_NAME: str
    DB_ENGINE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    DB_TABLE_PREFIX: str

    DB_ECHO_MODE: bool
    DB_POOL_SIZE: int

    DB_URL: str = ''
    DB_TEST_URL: str = ''

    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class LoggingConfig(CustomSettings):
    LOGGING_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    LOGGING_FORMAT: str
    LOGGER: logging.Logger = logging.getLogger(__name__)

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.LOGGING_LEVEL]


class RunConfig(CustomSettings):
    app_src: AppRunConfig = AppRunConfig()


class Tags(CustomSettings):
    TECH_TAG: str
    ROOT_TAG: str
    SWAGGER_TAG: str

    AUTH_PREFIX: str
    AUTH_TAG: str


class Settings(CustomSettings):
    app: AppSettings = AppSettings()
    logging: LoggingConfig = LoggingConfig()
    run: RunConfig = RunConfig()
    tags: Tags = Tags()
    db: DB = DB()
    auth: Auth = Auth()


settings = Settings()


def get_db_connection(db_name: str) -> str:
    return '{}://{}:{}@{}:{}/{}'.format(
        settings.db.DB_ENGINE,
        settings.db.DB_USER,
        settings.db.DB_PASSWORD,
        settings.db.DB_HOST,
        settings.db.DB_PORT,
        db_name,
    )


settings.db.DB_URL = get_db_connection(settings.db.DB_NAME)
