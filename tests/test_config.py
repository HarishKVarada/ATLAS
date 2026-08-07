from atlas.config import get_settings


def test_default_environment_is_development(monkeypatch):
    monkeypatch.delenv("ATLAS_ENV", raising=False)

    settings = get_settings()

    assert settings.environment == "development"


def test_environment_override_is_lowercase(monkeypatch):
    monkeypatch.setenv("ATLAS_ENV", "TEST")

    settings = get_settings()

    assert settings.environment == "test"


def test_environment_override_strips_whitespace(monkeypatch):
    monkeypatch.setenv("ATLAS_ENV", "  TEST  ")

    settings = get_settings()

    assert settings.environment == "test"


def test_blank_environment_falls_back_to_development(monkeypatch):
    monkeypatch.setenv("ATLAS_ENV", "   ")

    settings = get_settings()

    assert settings.environment == "development"
