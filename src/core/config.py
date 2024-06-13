from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent
env_file_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_file_path)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

REDIS_URL_EMAIL_CONFIRMATIONS = os.getenv("REDIS_URL_EMAIL_CONFIRMATIONS")
REDIS_URL_PASSWORD_RECOVERY = os.getenv("REDIS_URL_PASSWORD_RECOVERY")

API_PREFIX = "/api/v1"

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

COOKIE_TIME_EXPIRE = 60 * 60 * 24 * 120

YOOKASSA_ID = "test_yookassa_id"
YOOKASSA_SECRET_KEY = "test_yookassa_secret_key"
YOOKASSA_REDIRECT_URL = "test_yookassa_redirect_url"


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 24 * 60
    refresh_token_expire_days: int = 30


class SmtpSettings(BaseModel):
    smtp_server: str = os.getenv("SMTP_SERVER")
    smtp_port: int = os.getenv("SMTP_PORT")
    smtp_username: str = os.getenv("SMTP_USERNAME")
    smtp_password: str = os.getenv("SMTP_PASSWORD")


class AISettings(BaseModel):
    ai_url: str = os.getenv("AI_URL")
    ai_api_key: str = os.getenv("AI_API_KEY")
    ai_secret_key: str = os.getenv("AI_SECRET_KEY")
    ai_model_request: str = 'key/api/v1/models'
    ai_model_run: str = 'key/api/v1/text2image/run'
    ai_model_status: str = 'key/api/v1/text2image/status/'
    ai_model_headers: dict = {
        'X-Key': f'Key {ai_api_key}',
        'X-Secret': f'Secret {ai_secret_key}',
        'content_type': 'multipart/form-data'
    }


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

    smtp_settings: SmtpSettings = SmtpSettings()

    ai_setting: AISettings = AISettings()

    # db_echo: bool = True


settings = Settings()
