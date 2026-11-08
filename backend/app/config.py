import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    environment: str = field(default_factory=lambda: os.getenv("APP_ENV", "local"))
    origin: str = field(
        default_factory=lambda: os.getenv("PUBLIC_APP_ORIGIN", "http://localhost:3000")
    )
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://plantly:local-development-only@127.0.0.1:5432/plantly",
        )
    )
    gemini_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""), repr=False)
    gemini_model: str = field(default_factory=lambda: os.getenv("GEMINI_GENERATION_MODEL", ""))
    ai_enabled: bool = field(
        default_factory=lambda: os.getenv("AI_ENABLED", "false").lower() == "true"
    )

    def __post_init__(self):
        if self.environment != "local" and not self.origin.startswith("https://"):
            raise ValueError("Non-local environments require an HTTPS public origin")

    @property
    def cookie_name(self):
        return "plantly_session_dev" if self.environment == "local" else "__Host-plantly_session"


settings = Settings()
