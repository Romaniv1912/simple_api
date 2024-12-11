import inspect
import logging
import os

from sys import stderr, stdout

from asgi_correlation_id import correlation_id
from loguru import logger

from src.common.settings import LogSettings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(settings: LogSettings):
    """
    From https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    https://github.com/pawamoy/pawamoy.github.io/issues/17
    """
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.ROOT_LEVEL)

    no_propagate = ('watchfiles.main',)  # 'uvicorn.access')

    # Remove all log handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        if any(map(lambda x: x in name, no_propagate)):
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        # Debug log handlers
        # logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    # Remove every other logger's handlers
    logger.remove()

    # Define the correlation_id filter function
    # https://github.com/snok/asgi-correlation-id?tab=readme-ov-file#configure-logging
    # https://github.com/snok/asgi-correlation-id/issues/7
    def correlation_id_filter(record) -> bool:
        cid = correlation_id.get(settings.CID_DEFAULT_VALUE)
        record['correlation_id'] = cid[: settings.CID_UUID_LENGTH]
        return True

    # Configure loguru logger before starts logging
    logger.configure(
        handlers=[
            {
                'sink': stdout,
                'level': settings.STDOUT_LEVEL,
                'filter': lambda record: correlation_id_filter(record) and record['level'].no <= 25,
                'format': settings.STD_FORMAT,
            },
            {
                'sink': stderr,
                'level': settings.STDERR_LEVEL,
                'filter': lambda record: correlation_id_filter(record) and record['level'].no >= 30,
                'format': settings.STD_FORMAT,
            },
        ]
    )


def set_customize_logfile(log_path: str, settings: LogSettings):
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # log files
    log_stdout_file = os.path.join(log_path, settings.STDOUT_FILENAME)
    log_stderr_file = os.path.join(log_path, settings.STDERR_FILENAME)

    # loguru logger: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = {
        'rotation': '10 MB',
        'retention': '15 days',
        'compression': 'tar.gz',
        'enqueue': True,
        'format': settings.LOGURU_FORMAT,
    }

    # stdout file
    logger.add(
        str(log_stdout_file),
        level=settings.STDOUT_LEVEL,
        **log_config,
        backtrace=False,
        diagnose=False,
    )

    # stderr file
    logger.add(
        str(log_stderr_file),
        level=settings.STDERR_LEVEL,
        **log_config,
        backtrace=True,
        diagnose=True,
    )


log = logger
