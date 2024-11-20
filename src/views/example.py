from __future__ import annotations
import json
import os
from typing import Optional
from aws_lambda_powertools import Logger
from fastapi import APIRouter

from src.data_access.local_cache import get_ssm_param
from src.utils.decorators import long_running_task
from src.utils.encoders import MongoDBJSONEncoder
from src.utils.sns import publish_message
import boto3

router = APIRouter()
logger = Logger()


@router.post('/example/process-task')
@long_running_task
def process_task(data: dict, response_task_id: Optional[str] = None):
    try:
        logger.info("Sending SNS notification to process task")
        payload = {
            "data": data,
            "response_task_id": response_task_id,
        }
        payload = json.loads(json.dumps(payload, cls=MongoDBJSONEncoder))
        publish_message(
            client=boto3.client('sns'),
            topic_arn=get_ssm_param(key=f"/{os.getenv('API_STAGE')}/v1/sns/system_event_topic_arn"),
            subject="example_event",
            default_message=payload
        )
        logger.info("SNS notification sent")
    except Exception as e:
        logger.warning(f"[LUMIGO_LOG] Failed to send SNS notification: {e}")
