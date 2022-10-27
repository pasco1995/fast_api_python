from pydantic import BaseSettings


class Settings(BaseSettings):

    def __init__(self, _env_file):
        super().__init__(_env_file)

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings('.env')