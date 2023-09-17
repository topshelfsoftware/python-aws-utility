import logging
from typing import List, Union

from boto3.session import Session as Boto3Session
from botocore.client import BaseClient
from botocore.exceptions import ClientError as BotoClientError

from topshelfsoftware_aws_util.secrets import logger as secrets_logger
from topshelfsoftware_aws_util.sfn import logger as sfn_logger
from topshelfsoftware_aws_util.ssm import logger as ssm_logger
from topshelfsoftware_util.log import get_logger

PACKAGE_NAME = "topshelfsoftware-aws-util"

logger = get_logger(PACKAGE_NAME, stream=None)


def create_boto3_client(service_name: str, region: str = None) -> BaseClient:
    """Create a low-level service client by name.

    Parameters
    ----------
    service_name: str
        Name of the AWS service.
    
    region: str, optional
        Region where service abides.
        Default is `None`.
    
    Returns
    -------
    botocore.client.BaseClient
        AWS low-level service client.
    """
    logger.debug(f"creating boto3 client: {service_name}")
    try:
        session = Boto3Session(region_name=region)
        client = session.client(service_name=service_name)
    except BotoClientError as e:
        logger.error(f"failed to create client: {service_name}. Reason: {e}")
        raise e
    logger.debug("boto3 client successfully created")
    return client


def debug():
    """Set the package Loggers to the DEBUG level."""
    _set_logger_levels(level=logging.DEBUG)
    return


def get_package_loggers() -> List[logging.Logger]:
    """Retrieve a list of the Loggers used in the package."""
    loggers = [
        logger, secrets_logger, sfn_logger, ssm_logger
    ]
    return loggers


def _set_logger_levels(level: Union[int, str]):
    loggers = get_package_loggers()
    for logger in loggers:
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
    return
