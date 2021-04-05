import logging
import random
from time import sleep

from data_sources import ChromeSeleniumDataSource
from item_finder import ItemFinder
from metadata_providers import AbstractMetadataProvider
from notifications import AbstractNotifier


class Application(object):

    def __init__(self, metadata_provider: AbstractMetadataProvider, notifier: AbstractNotifier, query_url: str):
        self.metadata_provider = metadata_provider
        self.notifier = notifier
        self.query_url = query_url
        self.previous_message = None

    def __publish(self, results):
        subject = "Found items matching your requirements"
        lines = list()
        for i, result in enumerate(results):
            lines.append(str(i + 1) + ". " + str(result))
        message = "\n".join(lines)

        if message == self.previous_message:
            logging.info("Repeated message: {} ".format(message))
        else:
            self.notifier.publish(subject, message)
            self.previous_message = message
            logging.info("Message: {} ".format(message))

    def run(self):
        """
            1. Pick some random credentials
            2. Execute valid queries.
            3. Wait for a random time period (5-10 min)
            4. With some small probability go to step 1. Else step 2.
        """
        while True:
            try:
                username, password = random.choice(self.metadata_provider.get_all_accounts())
                data_source = ChromeSeleniumDataSource(username=username, password=password, query_url=self.query_url)
                while True:
                    try:
                        queries = self.metadata_provider.get_all_queries()
                        item_finder = ItemFinder(data_source=data_source, queries=queries)
                        result = item_finder.find_anomalies()
                        if result:
                            self.__publish(result)
                    except Exception as e:
                        logging.error(e)
                        pass
                    finally:
                        sleep(random.randint(5 * 60, 10 * 60))

                    if random.random() <= 0.1:  # 10% chance to choose credentials again
                        break
                del data_source
            except Exception as e:
                logging.error(e)
                pass
