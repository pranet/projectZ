from metadata_providers import GoogleSheetsMetaDataProvider, HybridMetaDataProvider


class MetadataProvidersFactory(object):

    @staticmethod
    def get_google_sheets_metadata_provider(developer_key: str, sheet_id: str) -> GoogleSheetsMetaDataProvider:
        return GoogleSheetsMetaDataProvider(developer_key=developer_key, sheet_id=sheet_id)

    @staticmethod
    def get_hybrid_metadata_provider(username: str, password: str, developer_key: str,
                                     sheet_id: str) -> HybridMetaDataProvider:
        accounts = [[username, password]]
        return HybridMetaDataProvider(accounts=accounts, developer_key=developer_key,
                                      sheet_id=sheet_id)
