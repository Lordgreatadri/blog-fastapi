#https://docs.pydantic.dev/2.7/migration/#other-changes
from pydantic_settings import BaseSettings  #{from pydantic import BaseSettings} =>this is version 1 imports

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings() 

