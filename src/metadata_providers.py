from abc import ABC, abstractmethod

from googleapiclient.discovery import build
from models import Query
import logging


class AbstractMetadataProvider(ABC):
    @abstractmethod
    def get_all_accounts(self) -> list:
        pass

    @abstractmethod
    def get_all_queries(self) -> list:
        pass


class GoogleSheetsMetaDataProvider(AbstractMetadataProvider):

    def __init__(self, sheet_id: str, developer_key: str):
        self.sheet_id = sheet_id
        self.service = build('sheets', 'v4', developerKey=developer_key)

    def __query_sheets(self, _range: str):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id, range=_range).execute()
        return result.get('values')

    def get_all_accounts(self) -> list:
        return self.__query_sheets('Accounts!A:ZZ')

    def get_all_queries(self) -> list:
        data = self.__query_sheets('Queries!A:ZZ')
        result = list()
        for entry in data:
            try:
                result.append(Query(keyword=entry[0], maximum_price=int(entry[1]), ignore=entry[2:]))
            except:
                logging.error("Failed to process row {}".format(entry))
        return result


class TestMetaDataProvider(AbstractMetadataProvider):

    def __init__(self, accounts: list, queries: list):
        self.accounts = accounts
        self.queries = queries

    def get_all_accounts(self) -> list:
        return self.accounts

    def get_all_queries(self) -> list:
        return self.queries


class HybridMetaDataProvider(AbstractMetadataProvider):

    def __init__(self, accounts: list, sheet_id: str, developer_key: str):
        self.test_provider = TestMetaDataProvider(accounts=accounts, queries=[])
        self.sheets_provider = GoogleSheetsMetaDataProvider(sheet_id=sheet_id, developer_key=developer_key)

    def get_all_accounts(self) -> list:
        return self.test_provider.get_all_accounts()

    def get_all_queries(self) -> list:
        return self.sheets_provider.get_all_queries()
