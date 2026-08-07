import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = "development"


def get_settings() -> Settings:
    environment = os.getenv("ATLAS_ENV", "").strip().lower()
    return Settings(environment=environment or "development")
