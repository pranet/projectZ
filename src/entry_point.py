import configparser
import logging
import os

from application import Application
from metadata_providers_factory import MetadataProvidersFactory
from notifications import SNSNotifier


def get_metadata_provider(config):
    if os.environ["ENVIRONMENT"] == "PRODUCTION":
        developer_key = config['DEFAULT']['developer_key']
        sheet_id = config['DEFAULT']['sheet_id']
        metadata_provider = MetadataProvidersFactory.get_google_sheets_metadata_provider(developer_key=developer_key,
                                                                                         sheet_id=sheet_id)
    elif os.environ["ENVIRONMENT"] == "LOCAL":
        username = os.environ["GAME_USERNAME"]
        password = os.environ["GAME_PASSWORD"]
        developer_key = config['DEFAULT']['developer_key']
        sheet_id = config['DEFAULT']['sheet_id']
        metadata_provider = MetadataProvidersFactory.get_hybrid_metadata_provider(username=username, password=password,
                                                                                  developer_key=developer_key,
                                                                                  sheet_id=sheet_id)
    elif os.environ["ENVIRONMENT"] == "TEST":
        raise NotImplementedError
    else:
        raise EnvironmentError("Please specify valid ENVIRONMENT env var")
    return metadata_provider


def get_notifier(config):
    sns_arn = config['DEFAULT']['sns_arn']
    return SNSNotifier(arn=sns_arn)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S")
    config = configparser.ConfigParser()
    config.read('resources/application.properties')
    Application(metadata_provider=get_metadata_provider(config), notifier=get_notifier(config),
                query_url=config['DEFAULT']['query_url']).run()
