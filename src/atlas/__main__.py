import logging

from atlas import get_version
from atlas.config import get_settings
from atlas.logging_config import configure_logging


def main() -> None:
    settings = get_settings()
    configure_logging()
    logger = logging.getLogger("atlas")

    logger.info("ATLAS v%s", get_version())
    logger.info("Environment: %s", settings.environment)
    logger.info("Status: READY")


if __name__ == "__main__":
    main()
