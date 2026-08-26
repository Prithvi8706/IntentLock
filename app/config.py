from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    model_primary: str = "local-deterministic"
    app_env: str = "development"
    ledger_path: Path = Path("audit/ledger.jsonl")


settings = Settings()

