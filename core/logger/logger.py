import logging


def set_logging_level(logging_level_str="debug"):
    logger = logging.getLogger("slice")
    logger.disabled = False
    if logging_level_str:
        logging_level = getattr(logging, logging_level_str.upper(), None)
        if logging_level is not None:
            logger.setLevel(logging_level)

            console_handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        else:
            print("Invalid logging level specified.")
    else:
        print("Logging level not specified.")


def get_logger():
    return logging.getLogger("slice")
