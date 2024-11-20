import boto3
from cachetools import cached, TTLCache
from aws_lambda_powertools import Logger

logger = Logger()

@cached(cache=TTLCache(maxsize=512, ttl=600))
def get_ssm_param(key, decrypt=False):
    """
        Get SSM parameter from AWS SSM Parameter Store
        :param key: SSM parameter key
        :param decrypt: Decrypt the SSM parameter
        :return: SSM parameter value
    """
    try:
        ssm_client = boto3.client('ssm')
        param = ssm_client.get_parameter(Name=key, WithDecryption=decrypt)
        return param[key]['Parameter']['Value']
    except Exception as e:
        logger.error(f"Failed to get SSM parameter: {key}, Exception: {e}")
