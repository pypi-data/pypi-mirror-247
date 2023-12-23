"""Abstraction layer on top of AWS Cloud Watch."""
import logging

import boto3

from botocore.exceptions import ClientError

# noinspection PyPackageRequirements
from pythonjsonlogger import jsonlogger

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOG_HANDLER = logging.StreamHandler()
FORMATTER = jsonlogger.JsonFormatter()
LOG_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOG_HANDLER)


class CloudWatchService:
    """Main class to handle AWS Cloudwatch communication."""

    def __init__(self):
        """Initialize default class variables - boto3 client for cloudwatch."""
        self.__cloudwatch_service = boto3.client("cloudwatch")

    def put_metric(self, metric: list, name_space: str):
        """Put a metric to the AWS Cloudwatch.

        :param metric: value of the metric
        :param name_space: The name space - catalog to which the metric will be placed
        :return:
        """
        try:
            self.__cloudwatch_service.put_metric_data(MetricData=metric, Namespace=name_space)
        except ClientError as error:
            LOGGER.error("Failed to put metric data: %s", metric)
            LOGGER.error("Failed to put metric in to namespace: %s", name_space)
            raise error
