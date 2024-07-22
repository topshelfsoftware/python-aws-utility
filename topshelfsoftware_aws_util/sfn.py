"""Facilitate interactions with Step Functions."""

from enum import Enum
import json
import uuid

from topshelfsoftware_aws_util.client import create_boto3_client
from topshelfsoftware_util.common import delay
from topshelfsoftware_util.json import fmt_json
from topshelfsoftware_util.log import get_logger

sfn_client = create_boto3_client("stepfunctions")
logger = get_logger(__name__, stream=None)


class SfnStatus(str, Enum):
    """Enumeration for step function status."""

    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    ABORTED = "ABORTED"


def launch_sfn(state_machine_arn: str, payload: dict, name: str = None) -> str:
    """Launch the step function with the specified payload.

    Parameters
    ----------
    state_machine_arn: str
        The ARN of the state machine.

    payload: dict
        Payload input to supply to the state machine.

    name: str, Optional
        The execution name of the state machine.
        Default of `None` generates a random UUID for the name.

    Returns
    -------
    str
        Step Functions execution ARN.
    """
    name = str(uuid.uuid4()) if name is None else name
    logger.info(f"Execution name: {name}")

    # run step function
    logger.info(f"Launching step function: {state_machine_arn}")
    res = sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        name=name,
        input=json.dumps(payload),
    )

    # retrieve the execution arn for the step function
    execution_arn = res["executionArn"]
    logger.info(f"execution arn: {execution_arn}")
    return execution_arn


def poll_sfn(execution_arn: str, step: float = 1) -> dict:
    """Poll the step function for status.
    Return the execution response once the status is no longer `RUNNING`.

    Parameters
    ----------
    execution_arn: str
        Step Functions execution ARN.

    step: float, Optional
        Amount of time (in sec) to wait between poll attempts.
        Default is 1 second.

    Returns
    -------
    dict
        Step Functions execution response.
    """
    sfn_status = SfnStatus.RUNNING.value
    n = 0
    while sfn_status == SfnStatus.RUNNING.value:
        delay(step)
        n += 1

        logger.debug(f"polling execution arn: {execution_arn}")
        res = sfn_client.describe_execution(executionArn=execution_arn)
        logger.info(f"poll #{n:02d} response: {fmt_json(res)}")

        sfn_status = res["status"]
    logger.info(f"sfn status: {sfn_status}")
    return res


def get_exec_hist(execution_arn: str, max_results: int = 5) -> dict:
    """Retrieve the step function execution history.

    Parameters
    ----------
    execution_arn: str
        Step Functions execution ARN.

    max_results: int, Optional
        Number of events to retrieve from the execution.
        Default is 5.

    Returns
    -------
    dict
        Step Functions execution history.
    """
    exec_history = sfn_client.get_execution_history(
        executionArn=execution_arn, maxResults=max_results, reverseOrder=True
    )
    logger.info(f"execution history: {fmt_json(exec_history)}")
    return exec_history
