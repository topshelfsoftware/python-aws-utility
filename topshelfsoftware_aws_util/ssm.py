"""Facilitate interactions with Systems Manager."""

from botocore.exceptions import ClientError as BotoClientError

from topshelfsoftware_aws_util import create_boto3_client
from topshelfsoftware_util.json import fmt_json
from topshelfsoftware_util.log import get_logger

ssm_client = create_boto3_client(service_name="ssm")
logger = get_logger(__name__, stream=None)


def get_ssm_value(name: str) -> str:
    """Retrieve the value of an SSM parameter.

    Parameters
    ----------
    name: str
        Name of the SSM parameter.
    
    Returns
    -------
    str
        Parameter store value.
    """
    logger.debug(f"getting ssm: {name}")
    try:
        ssm_resp = ssm_client.get_parameter(Name=name)
        logger.debug(f"resp: {fmt_json(ssm_resp)}")
        val = ssm_resp["Parameter"]["Value"]
    except BotoClientError as e:
        logger.error(f"failed to retrieve ssm parameter: {name}. Reason: {e}")
        raise e
    except KeyError as e:
        logger.error(f"failed to retrieve parameter value from ssm response: {name}. Reason: {e}")
        raise e
    logger.debug(f"ssm parameter value: {val}")
    return val
