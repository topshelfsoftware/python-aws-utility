import json
import logging
import os
import sys

from botocore.stub import Stubber
import pytest

from topshelfsoftware_aws_util.sfn import logger as sfn_logger
from topshelfsoftware_logging import add_log_stream, get_logger
from topshelfsoftware_polling.polling import logger as polling_logger
from topshelfsoftware_polling.step import (
    step_constant,  # noqa: F401, not used explicitly, evaluated at runtime
    step_exponential_backoff,  # noqa: F401, same as above
)
from topshelfsoftware_util.common import logger as common_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "sfn"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)
add_log_stream(sfn_logger, level=logging.DEBUG, stream=sys.stdout)
add_log_stream(polling_logger, level=logging.DEBUG, stream=sys.stdout)
add_log_stream(common_logger, level=logging.DEBUG, stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_aws_util.sfn import (  # noqa: E402
    sfn_client,
    launch_sfn,
    poll_sfn,
    get_exec_hist,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["launch_sfn"]),
)
def test_01_launch_sfn(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resp: dict = get_event_as_dict["input"]["stub"]["response"]
    expected_output: dict = get_event_as_dict["expected_output"]

    # Stub the boto3 client
    stubber = Stubber(sfn_client)
    stubber.add_response(stub_method, stub_resp, stub_params)

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        execution_arn = launch_sfn(
            stub_params["stateMachineArn"],
            json.loads(stub_params["input"]),
            stub_params["name"],
        )
        assert execution_arn == expected_output["execution_arn"]
    finally:
        # Deactivate the stubber
        stubber.deactivate()


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll_sfn"]),
)
def test_02_poll_sfn(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resps: list[dict] = get_event_as_dict["input"]["stub"]["responses"]
    poll_kwargs: dict = get_event_as_dict["input"]["poll_kwargs"]
    if "step_fun" in poll_kwargs:
        poll_kwargs["step_fun"] = eval(poll_kwargs["step_fun"])
    expected_output: dict = get_event_as_dict["expected_output"]

    # Stub the boto3 client
    stubber = Stubber(sfn_client)
    for stub_resp in stub_resps:
        stubber.add_response(stub_method, stub_resp, stub_params)

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        sfn_resp = poll_sfn(stub_params["executionArn"], **poll_kwargs)
        assert sfn_resp == expected_output
    finally:
        # Deactivate the stubber
        stubber.deactivate()


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["get_exec_hist"]),
)
def test_03_get_exec_hist(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    stub_method: str = get_event_as_dict["input"]["stub"]["method"]
    stub_params: dict = get_event_as_dict["input"]["stub"]["parameters"]
    stub_resp: dict = get_event_as_dict["input"]["stub"]["response"]
    expected_output: dict = get_event_as_dict["expected_output"]

    # Stub the boto3 client
    stubber = Stubber(sfn_client)
    stubber.add_response(stub_method, stub_resp, stub_params)

    try:
        # Activate the stubber
        stubber.activate()

        # Test the source code
        events = get_exec_hist(
            stub_params["executionArn"],
        )
        assert events == expected_output
    finally:
        # Deactivate the stubber
        stubber.deactivate()
