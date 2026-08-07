from atlas import get_version


def test_get_version_returns_current_project_version():
    assert get_version() == "0.1.0-dev"
