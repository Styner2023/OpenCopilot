from typing import Any, Optional
from routes.workflow.typings.response_dict import ResponseDict
from routes.workflow.typings.run_workflow_input import FlowData
from routes.workflow.utils.run_openapi_ops import run_actions
from opencopilot_types.workflow_type import WorkflowDataType
from werkzeug.datastructures import Headers
import logging
import json

from utils.get_logger import CustomLogger

logger = CustomLogger(module_name=__name__)


async def run_flow(
    workflow_doc: WorkflowDataType,
    data: FlowData,
    app: Optional[str],
    bot_id: str,
) -> ResponseDict:
    headers = data.headers or Headers()

    result = ""
    error = None

    try:
        result = await run_actions(
            workflow_doc,
            data.text,
            headers,
            app,
            bot_id=bot_id,
        )
    except Exception as e:
        payload_data = {
            "headers": dict(headers),
            "app": app,
        }

        error_data = {
            "payload": json.dumps(payload_data),
            "error": str(e),
            "incident": "run_workflow",
        }

        logger.error("An exception occurred", error=error_data)
        error = str(e)

    output: ResponseDict = {"response": result if not error else "", "error": error}

    logging.info(
        "Workflow output %s", json.dumps(output, separators=(",", ":"))
    )

    return output
