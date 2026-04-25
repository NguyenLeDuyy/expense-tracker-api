import logging
import sys

def setup_logging():
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger("app")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    return root_logger