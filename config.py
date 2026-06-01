# """
# Application settings loaded from environment variables.
# Values are read from a .env file in development; set directly in staging/production.
# """

# import os

# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL: str = os.environ["DATABASE_URL"]
# APP_ENV: str = os.getenv("APP_ENV", "development")


""" "pydantic"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    app_env: str = "Development"
    jwt_algorithm: str
    jwt_expiry_minutes: int
    jwt_Secret: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


setting = Settings()
