"""Facilitate interactions with Step Functions."""

from enum import Enum
import json
from typing import Callable, Optional, Tuple
import uuid

from topshelfsoftware_aws_util.client import create_boto3_client
from topshelfsoftware_logging import get_logger
from topshelfsoftware_polling.polling import poll
from topshelfsoftware_polling.step import step_exponential_backoff
from topshelfsoftware_util.json import fmt_json

sfn_client = create_boto3_client("stepfunctions")
logger = get_logger(__name__, stream=None)


class SfnStatus(str, Enum):
    """Enumeration for step function status."""

    WAITING = "WAITING"  # valid if using an Express Workflow
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    ABORTED = "ABORTED"

    @property
    def is_concluded(self):
        """Indicates the Step Function is done, but not necessarily succeeded.
        True if status is NOT in WAITING or RUNNING state;
        otherwise, False."""
        values = [
            SfnStatus.WAITING.value,
            SfnStatus.RUNNING.value,
        ]
        return self.value not in values


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


def status_sfn(execution_arn: str) -> dict:
    """Status the step function execution.

    Parameters
    ----------
    execution_arn: str
        Step Functions execution ARN.

    Returns
    -------
    dict
        Step Functions execution response.
    """
    logger.debug(f"statusing execution arn: {execution_arn}")
    res = sfn_client.describe_execution(executionArn=execution_arn)
    logger.debug(f"sfn execution response: {fmt_json(res)}")
    return res


def poll_sfn(
    execution_arn: str,
    step_fun: Callable = step_exponential_backoff,
    step_fun_kwargs: Optional[dict] = None,
    timeout: float = 300,
    max_attempts: Optional[int] = None,
    ignore_exceptions: Optional[Tuple[Exception, ...]] = None,
) -> dict:
    """Poll the step function for status.
    Return the execution response once the Step Function has concluded.

    Parameters
    ----------
    execution_arn: str
        Step Functions execution ARN.

    step_fun: Callable, optional
        A callback function to compute the next step in seconds.
        See `topshelfsoftware_polling.step` for predefined step functions.
        Default is `topshelfsoftware_polling.step.step_exponential_backoff`.

    step_fun_kwargs: dict, optional
        Step function kwargs.
        See `topshelfsoftware_polling.step` for predefined step functions
        and kwargs.
        Default is `None`.

    timeout: float, optional
        Length of poll in seconds.
        `topshelfsoftware_polling.exceptions.PollTimeLimitReached` raised
        if this timeout is exceeded.
        Default is `300`.

    max_attempts: int, optional
        Maximum number of times the target function
        `topshelfsoftware_aws_util.sfn.status_sfn` will be called
        before failing.
        `topshelfsoftware_polling.exceptions.PollAttemptLimitReached` raised
        if attempts exceeds this value.
        Default of `None` means poll with no limit for number of attempts.

    ignore_exceptions: tuple[Exception, ...], optional
        These exceptions are caught and ignored. Thus, the result is that
        a retry will be performed on the target function
        `topshelfsoftware_aws_util.sfn.status_sfn`.
        Default is `None`.

    Returns
    -------
    dict
        Step Functions execution response.
    """
    poll_kwargs = {
        "fun": status_sfn,
        "args": (execution_arn,),
        "step_fun": step_fun,
        "step_fun_kwargs": step_fun_kwargs,
        "timeout": timeout,
        "max_attempts": max_attempts,
        "check_success": lambda r: SfnStatus(r["status"]).is_concluded,
        "ignore_exceptions": ignore_exceptions,
    }
    res = poll(**poll_kwargs)
    logger.info(f"sfn response: {fmt_json(res)}")
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
