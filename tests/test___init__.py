import logging
import os
import sys

import pytest

from topshelfsoftware_util.log import get_logger

from conftest import get_json_files

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "__init__"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_aws_util import debug, get_package_loggers  # noqa: E402


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["debug"])
)
def test_01_debug(get_event_as_dict):
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    pkg_loggers = get_package_loggers()
    assert all(
        isinstance(pkg_logger, logging.Logger) for pkg_logger in pkg_loggers
    ), f"Not all elements are of type {logging.Logger}"

    debug()
    assert all(
        pkg_logger.level == logging.DEBUG for pkg_logger in pkg_loggers
    ), f"Not all loggers are at the {logging.DEBUG} level"
