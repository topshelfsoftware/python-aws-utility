import logging
import os
import sys

from botocore import exceptions as botoexceptions  # noqa: F401
import pytest

from topshelfsoftware_aws_util.client import logger as client_logger
from topshelfsoftware_logging import add_log_stream, get_logger

from conftest import get_json_files

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "client"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)
add_log_stream(client_logger, level=logging.DEBUG, stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_aws_util.client import (  # noqa: E402
    BaseClient,
    create_boto3_client,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["create_boto3_client", "client"]),
)
def test_01_create_boto3_client(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    svc_name: str = get_event_as_dict["input"]["service_name"]
    client = create_boto3_client(svc_name)
    assert isinstance(client, BaseClient)


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["create_boto3_client", "exc"]),
)
def test_02_create_boto3_client(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    service_name: str = get_event_as_dict["input"]["service_name"]
    region: str = get_event_as_dict["input"]["region"]
    exception: str = get_event_as_dict["input"]["exception"]

    with pytest.raises(eval(exception)):
        create_boto3_client(service_name, region)
