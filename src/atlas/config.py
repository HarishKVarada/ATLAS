from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    environment: str = "development"


def get_settings() -> Settings:
    environment = os.getenv("ATLAS_ENV", "").strip().lower()
    return Settings(environment=environment or "development")
