import json
import logging
import os
import arrow
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
import boto3

_CACHED_CONFIG_PARAMETERS = {}


def task_upsert_value(Model, task_id, task_value):
    """
    Upsert a task value to the cache
    :param Model:
    :param task_id:
    :param task_value:
    :return: response
    """
    model = Model()
    ttl = int(arrow.utcnow().shift(hours=1).timestamp())
    try:
        existing_item = model.get(task_id)
        existing_item.update(
            actions=[
                Model.cache_value.set(task_value),
                Model.ttl.set(ttl),
            ]
        )
    except Exception as e:
        model.task_id = task_id
        model.task_value = json.dumps(task_value)
        model.ttl = ttl
        model.save()


class LongRunningTasksModel(Model):
    """
    Model to store long running tasks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ssm_client = boto3.client('ssm')
        global _CACHED_CONFIG_PARAMETERS
        key = f"/{os.getenv('API_STAGE')}/core/tables/long_running_tasks_table"
        if _CACHED_CONFIG_PARAMETERS.get(key) is None:
            logging.info(f"Getting {key} from SSM")
            _CACHED_CONFIG_PARAMETERS[key] = ssm_client.get_parameter(Name=key)

        self.Meta.table_name = _CACHED_CONFIG_PARAMETERS[key]['Parameter']['Value']

    class Meta:
        table_name = ''

    task_id = UnicodeAttribute(hash_key=True)
    task_value = UnicodeAttribute(null=True)
    ttl = NumberAttribute()
