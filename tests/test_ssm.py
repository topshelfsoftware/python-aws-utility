import logging
import os
import sys

import botocore  # noqa: F401
from botocore.stub import Stubber
import pytest

from topshelfsoftware_aws_util.ssm import logger as ssm_logger
from topshelfsoftware_logging import add_log_stream, get_logger

from conftest import get_json_files

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "ssm"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)
add_log_stream(ssm_logger, level=logging.DEBUG, stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_aws_util.ssm import (  # noqa: E402
    ssm_client,
    get_ssm_value,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["get_ssm_value", "resp"]),
)
def test_01_get_ssm_value(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resp: dict = get_event_as_dict["input"]["stub"]["response"]
    expected_output: dict = get_event_as_dict["expected_output"]

    # Stub the boto3 client
    stubber = Stubber(ssm_client)
    stubber.add_response(stub_method, stub_resp, stub_params)

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        secret = get_ssm_value(stub_params["Name"])
        assert secret == expected_output["ssm_value"]
    finally:
        # Deactivate the stubber
        stubber.deactivate()


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["get_ssm_value", "key_err"]),
)
def test_02_get_ssm_value(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resp: dict = get_event_as_dict["input"]["stub"]["response"]

    # Stub the boto3 client
    stubber = Stubber(ssm_client)
    stubber.add_response(stub_method, stub_resp, stub_params)

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        with pytest.raises(KeyError):
            get_ssm_value(stub_params["Name"])
    finally:
        # Deactivate the stubber
        stubber.deactivate()


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["get_ssm_value", "exc"]),
)
def test_03_get_ssm_value(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resp: dict = get_event_as_dict["input"]["stub"]["response"]
    exception: str = get_event_as_dict["input"]["exception"]

    # Stub the boto3 client
    stubber = Stubber(ssm_client)
    stubber.add_client_error(
        stub_method,
        service_error_code=stub_resp["Error"]["Code"],
        service_message=stub_resp["Error"]["Message"],
        http_status_code=stub_resp["Error"]["HttpStatusCode"],
        expected_params=stub_params,
    )

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        with pytest.raises(eval(exception)):
            get_ssm_value(stub_params["Name"])
    finally:
        # Deactivate the stubber
        stubber.deactivate()
