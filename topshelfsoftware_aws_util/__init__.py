import logging
from typing import List, Union

from topshelfsoftware_aws_util.client import logger as client_logger
from topshelfsoftware_aws_util.secrets import logger as secrets_logger
from topshelfsoftware_aws_util.sfn import logger as sfn_logger
from topshelfsoftware_aws_util.ssm import logger as ssm_logger

PACKAGE_NAME = "topshelfsoftware-aws-util"


def debug():
    """Set the package Loggers to the DEBUG level."""
    _set_logger_levels(level=logging.DEBUG)
    return


def get_package_loggers() -> List[logging.Logger]:
    """Retrieve a list of the Loggers used in the package."""
    loggers = [
        client_logger, secrets_logger, sfn_logger, ssm_logger
    ]
    return loggers


def _set_logger_levels(level: Union[int, str]):
    loggers = get_package_loggers()
    for logger in loggers:
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
    return
