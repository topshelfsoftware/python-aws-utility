import configparser
import os
import sys

# add service and lambdas dir to system path, otherwise cannot import modules
PROJ_ROOT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
PACKAGE_PATH = os.path.join(PROJ_ROOT_PATH, "topshelfsoftware_aws_util")
sys.path.append(PROJ_ROOT_PATH)
sys.path.append(PACKAGE_PATH)

# test file paths
TESTS_PATH = os.path.join(PROJ_ROOT_PATH, "tests")
TEST_EVENTS_PATH = os.path.join(TESTS_PATH, "events")

# parse config.ini file if it exists to support aws-cli authentication
CONFIG_INI_PATH = os.path.join(TESTS_PATH, "config.ini")
if os.path.isfile(CONFIG_INI_PATH):
    config = configparser.RawConfigParser()
    config.read(CONFIG_INI_PATH)
    config_dict = dict(config.items("main"))
    for k, v in config_dict.items():
        os.environ[k.upper()] = v
