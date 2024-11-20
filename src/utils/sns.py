import json
from src.utils.encoders import MongoDBJSONEncoder

def publish_message(client, topic_arn, subject, default_message):
    """
    Publishes a multi-format message to a topic. A multi-format message takes
    different forms based on the protocol of the subscriber.

    :param topic_arn: The topic to publish to.
    :param client: SNS client
    :param subject: The subject of Тthe message.
    :param default_message: The default version of the message. This version is
                            sent to subscribers that have protocols that are not
                            otherwise specified in the structured message.
    :return: The ID of the message.
    """
    json_message = json.dumps({"default": json.dumps(default_message, cls=MongoDBJSONEncoder)})
    response = client.publish(
        TopicArn=topic_arn,
        Message=json_message,
        Subject=subject,
        MessageStructure='json')
    message_id = response['MessageId']
    return message_id