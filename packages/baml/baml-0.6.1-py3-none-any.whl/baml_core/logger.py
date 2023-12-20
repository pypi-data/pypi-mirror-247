# Set up module-specific logging
import logging
import coloredlogs

logger = logging.getLogger("baml")
logger.setLevel(logging.INFO)

# Custom field styles for coloredlogs
field_styles = {
    "asctime": {"color": "green"},
    "hostname": {"color": "magenta"},
    "levelname": {"color": "white", "bold": True},
    "name": {"color": "blue", "bold": True},
    "programname": {"color": "cyan"},
}
level_styles = {
    "warning": {"color": "yellow"},
    "error": {"color": "red"},
    "critical": {"color": "red", "bold": True},
}

coloredlogs.install(
    level="INFO",
    logger=logger,
    fmt="%(asctime)s - [BAML] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    field_styles=field_styles,
    level_styles=level_styles,
)
