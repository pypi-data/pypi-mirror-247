import logging

from patched_cli.utils.managed_files import LOG_FILE

# default noop logger
logger = logging.getLogger("patched_cli")
_noop = logging.NullHandler()
logger.addHandler(_noop)


def init_logger() -> logging.Logger:
    global logger, _noop
    logger.removeHandler(_noop)

    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, mode="w")
    formatter = logging.Formatter("%(asctime)s :: %(filename)s@%(funcName)s@%(lineno)d :: %(levelname)s :: %(msg)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
