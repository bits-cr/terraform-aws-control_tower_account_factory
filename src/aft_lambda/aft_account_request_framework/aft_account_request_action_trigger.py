# Copyright Amazon.com, Inc. or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import inspect
import logging
from typing import TYPE_CHECKING, Any, Dict

import aft_common.ssm
from aft_common import constants as utils
from aft_common import notifications
from aft_common.account_request_record_handler import AccountRequestRecordHandler
from aft_common.aft_utils import invoke_lambda, sanitize_input_for_logging
from aft_common.auth import AuthClient
from aft_common.logger import configure_aft_logger

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext
else:
    LambdaContext = object


configure_aft_logger()
logger = logging.getLogger("aft")


def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> None:
    auth = AuthClient()
    try:
        record_handler = AccountRequestRecordHandler(auth=auth, event=event)
        logger.info(sanitize_input_for_logging(record_handler.record))
        record_handler.process_request()

        # Invoke the processor right away instead of waiting for its schedule.
        # It ignores the payload and reads the queue itself, so a run with
        # nothing queued (e.g. customization-only requests) is a no-op.
        if record_handler.record["eventName"] in ("INSERT", "MODIFY"):
            processor_arn = aft_common.ssm.get_ssm_parameter_value(
                auth.aft_management_session,
                utils.SSM_PARAM_AFT_ACCOUNT_REQUEST_PROCESSOR_FUNCTION_ARN,
            )
            invoke_lambda(auth.aft_management_session, processor_arn, b"{}")

    except Exception as error:
        notifications.send_lambda_failure_sns_message(
            session=auth.aft_management_session,
            message=str(error),
            context=context,
            subject="AFT account request failed",
        )
        message = {
            "FILE": __file__.split("/")[-1],
            "METHOD": inspect.stack()[0][3],
            "EXCEPTION": str(error),
        }
        logger.exception(message)
        raise
