"""Facilitate interactions with Secrets Manager."""

from botocore.exceptions import ClientError as BotoClientError

from topshelfsoftware_aws_util.client import create_boto3_client
from topshelfsoftware_util.json import fmt_json
from topshelfsoftware_logging import get_logger

secret_client = create_boto3_client(service_name="secretsmanager")
logger = get_logger(__name__, stream=None)


def get_secret_value(secret_id: str) -> str:
    """Retrieve the value of a managed secret.

    Parameters
    ----------
    secret_id: str
        The ARN or name of the secret to retrieve.

    Returns
    -------
    str
        Secret value.
    """
    logger.debug(f"getting secret: {secret_id}")
    try:
        secret_resp = secret_client.get_secret_value(SecretId=secret_id)
        logger.debug(f"resp: {fmt_json(secret_resp)}")
        val = secret_resp["SecretString"]
    except BotoClientError as e:
        logger.error(f"failed to retrieve secret: {secret_id}. Reason: {e}")
        raise e
    except KeyError as e:
        logger.error(
            f"failed to retrieve string from secretsmanager response: "
            f"{secret_id}. Reason: {e}"
        )
        raise e
    logger.debug("secret string: <redacted>")
    return val
