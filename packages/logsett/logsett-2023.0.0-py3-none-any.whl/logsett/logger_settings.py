import logging
import sys
from os import environ
from loguru import logger


LOG_LEVEL = logging.getLevelName(environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(time_color='#676767', additional_params_color='#917b52', debug_color='#8d541c'):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    fmt = (
        f"<fg {time_color}>"
        "{time:YYYY-MM-DD HH:mm:ss.SSS}"
        f"</fg {time_color}> | "
        "<level>{level: <8}</level> | "
        f"<fg {additional_params_color}>"
        "{name}:{function}:{line}"
        f"</fg {additional_params_color}> | "
        "- <level>{message}</level>"
    )

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS, "format": fmt}])
    logger.level("DEBUG", color=f"<fg {debug_color}>")

setup_logging()