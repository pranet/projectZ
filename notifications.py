from abc import ABC, abstractmethod

import boto3


class AbstractNotifier(ABC):
    @abstractmethod
    def publish(self, subject: str, message: str):
        pass


class SNSNotifier(AbstractNotifier):
    def __init__(self, arn: str):
        self.arn = arn

    def publish(self, subject: str, message: str):
        client = boto3.client("sns", region_name="us-east-1")
        client.publish(
            TopicArn=self.arn,
            Message=message,
            Subject=subject
        )
