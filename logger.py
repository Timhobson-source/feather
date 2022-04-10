import logging


def setup_logger():
    logger = logging.getLogger("tim's logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s][%(name)s][%(filename)s, ln %(lineno)d]: %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


log = setup_logger()
