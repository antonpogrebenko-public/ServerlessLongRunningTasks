import json

from aws_lambda_powertools import Logger
from src.data_access.models import task_upsert_value, LongRunningTasksModel


logger = Logger()

def handle_example_event(payload):
    logger.info(f"Handling example event {payload}")

    task_upsert_value(Model=LongRunningTasksModel, task_id=payload["response_task_id"], task_value={
        "response": "xxx",
    })
    return

EVENT_PROCESSOR = {
    "example_event": [handle_example_event],
}


def consume_event(event, context):
    """
    Consume SNS event
    :param event:
    :param context:
    :return: None
    """
    logger.info(f"Received SNS event {event}")
    for record in event['Records']:
        sns_message = record.get("Sns", {}).get("Message")
        sns_subject = record.get("Sns", {}).get("Subject")

        if sns_message is not None:
            sns_message = json.loads(sns_message)
            sns_message['event'] = sns_subject
            if sns_subject in EVENT_PROCESSOR:
                for processor in EVENT_PROCESSOR[sns_subject]:
                    processor(sns_message)
            else:
                print(f"Event type {sns_subject} not supported")
        else:
            print("No SNS message found in event")
