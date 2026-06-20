from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    gemini_api_key: str = Field(alias="GEMINI_API_KEY")

    @field_validator("gemini_api_key")
    @classmethod
    def validate_gemini_key(cls, v: str) -> str:
        if not v or v in ("your_gemini_api_key_here", "test_key_for_demo"):
            print("WARNING: GEMINI_API_KEY is not set. AI scoring will fail.")
        return v
    gemini_model: str = Field(default="gemini-1.5-flash", alias="GEMINI_MODEL")
    resend_api_key: str | None = Field(default=None, alias="RESEND_API_KEY")
    email_from: str = Field(default="onboarding@resend.dev", alias="EMAIL_FROM")
    brightbean_url: str | None = Field(default=None, alias="BRIGHTBEAN_URL")
    n8n_webhook_url: str | None = Field(default=None, alias="N8N_WEBHOOK_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()