"""Facilitate interactions with low-level service clients."""

from boto3.session import Session as Boto3Session
from botocore.client import BaseClient
from botocore.exceptions import ClientError as BotoClientError

from topshelfsoftware_util.log import get_logger

logger = get_logger(__name__, stream=None)


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
