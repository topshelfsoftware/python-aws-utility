import glob
import json
import os
import shutil
import sys
from typing import Generator

import pytest
import yaml

import __setup__  # noqa: F401 - need __setup__ for sys path imports to work
from topshelfsoftware_logging import get_logger

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
FILE_DELIMITER = "-"

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger("conftest", stream=sys.stdout)


# ----------------------------------------------------------------------------#
#                                 --- MAIN ---                                #
# ----------------------------------------------------------------------------#
@pytest.fixture
def get_event_as_dict(
    event_dir: str, event_file: str
) -> Generator[dict, None, None]:
    """Read a JSON-formatted file into a Python dictionary."""
    event_fp = os.path.join(event_dir, event_file)
    event = convert_json_to_dict(event_fp)
    yield event


@pytest.fixture
def get_event_as_str(
    event_dir: str, event_file: str
) -> Generator[str, None, None]:
    """Read a JSON-formatted file into a Python string."""
    event_fp = os.path.join(event_dir, event_file)
    logger.info(f"reading JSON file {event_file} into string")
    with open(event_fp, "r") as fp:
        event = fp.read()
    yield event


def get_json_files(dirname: str, matching: list[str] = None) -> list[str]:
    """Obtain all json files or a subset of the json files
    matching the provided string."""
    all_event_files = [
        os.path.basename(x)
        for x in sorted(glob.glob(os.path.join(dirname, "*.json")))
    ]
    subset = []
    for file_name in all_event_files:
        file_no_ext, _ = os.path.splitext(file_name)
        file_kw = file_no_ext.split(FILE_DELIMITER)
        if matching is None or set(matching).issubset(set(file_kw)):
            subset.append(file_name)
    return subset


def convert_json_to_dict(json_fp: str) -> dict:
    """Read a JSON-formatted file into a Python dictionary."""
    logger.info(f"reading JSON file {json_fp} into dict")
    with open(json_fp, "r") as fp:
        json_dict = json.load(fp)
    return json_dict


def convert_yaml_to_dict(yaml_fp: str) -> dict:
    """Read a YAML-formatted file into a Python dictionary."""
    logger.info(f"reading YAML file {yaml_fp} into dict")
    with open(yaml_fp, "r") as fp:
        yaml_dict = yaml.safe_load(fp)
    return yaml_dict


def print_section_break(char: str = "-") -> str:
    """Print a section break the width of the terminal
    by using a string of characters."""
    terminal_width = shutil.get_terminal_size().columns
    section_break_str = char * terminal_width
    print(section_break_str)
