"""Facilitate interactions with Systems Manager."""

from botocore.exceptions import ClientError as BotoClientError

from topshelfsoftware_aws_util.client import create_boto3_client
from topshelfsoftware_logging import get_logger
from topshelfsoftware_util.json import fmt_json

ssm_client = create_boto3_client(service_name="ssm")
logger = get_logger(__name__, stream=None)


def get_ssm_value(name: str, with_decryption: bool = False) -> str:
    """Retrieve the value of an SSM parameter.

    Parameters
    ----------
    name: str
        Name of the SSM parameter.

    with_decryption: bool, optional
        When `True` the parameter value will be decrypted if it is a
        SecureString. If `False`, the encrypted ciphertext will be
        returned as is. Note: `True` is also acceptable if the parameter
        is not a SecureString, in which case it will simply return the
        plaintext value.
        Defaults to `False`.

    Returns
    -------
    str
        Parameter store value.
    """
    logger.debug(f"getting ssm: {name}")
    try:
        ssm_resp = ssm_client.get_parameter(
            Name=name, WithDecryption=with_decryption
        )
        logger.debug(f"resp: {fmt_json(ssm_resp)}")
        val = ssm_resp["Parameter"]["Value"]
        type_ = ssm_resp["Parameter"]["Type"]
    except BotoClientError as e:
        logger.error(f"failed to retrieve ssm parameter: {name}. Reason: {e}")
        raise e
    except KeyError as e:
        logger.error(
            f"failed to retrieve parameter value from ssm response: "
            f"{name}. Reason: {e}"
        )
        raise e
    (
        logger.debug(f"ssm parameter value: {val}")
        if type_ != "SecureString"
        else logger.debug("ssm parameter value: <redacted>")
    )
    return val
