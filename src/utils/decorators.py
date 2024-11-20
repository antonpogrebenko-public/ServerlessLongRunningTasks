import json
from aws_lambda_powertools import Logger
from src.data_access.models import LongRunningTasksModel
from src.views import __version__
import uuid
from functools import wraps

logger = Logger()


def long_running_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper for long running tasks. If task_id is provided, return the task status. Otherwise, create a new task
        :param args:
        :param kwargs:
        :return:
        """
        task_id = kwargs.get('data', {}).get('task_id', None)

        if task_id:
            try:
                response = LongRunningTasksModel().get(hash_key=f"{task_id}").task_value
                response = json.loads(response)
                return {
                    "api_version": f"{__version__}",
                    "message": response,
                    "task_status": "completed",
                    "task_id": task_id,
                    "statusCode": 200
                }
            except Exception as e:
                return {
                    "api_version": f"{__version__}",
                    "task_id": task_id,
                    "task_status": "pending",
                    "statusCode": 200
                }
        else:
            new_task_id = str(uuid.uuid4())
            kwargs['response_task_id'] = new_task_id
            func(*args, **kwargs)

            return {
                "api_version": f"{__version__}",
                "task_id": new_task_id,
                "task_status": "created",
                "statusCode": 200
            }

    return wrapper