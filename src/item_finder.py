from data_sources import AbstractDataSource


class ItemFinder(object):
    def __init__(self, data_source: AbstractDataSource, queries: list):
        self.data_source = data_source
        self.queries = queries

    @staticmethod
    def __filter_irrelevant_entries(data, keyword, _filter: list) -> list:
        for i in range(len(_filter)):
            _filter[i] = _filter[i].lower()
        keyword = keyword.lower()
        filtered = []
        for entry in data:
            text = entry.name.lower()
            changed = True
            while changed:
                changed = False
                for word in _filter:
                    if word != "" and word in text:
                        text = text.replace(word, "")
                        changed = True
            if keyword in text:
                filtered.append(entry)
        return filtered

    @staticmethod
    def __filter_overpriced_entries(data, maximum_price: int) -> list:
        filtered = []
        for entry in data:
            if entry.price <= maximum_price:
                filtered.append(entry)
        return filtered

    def __search(self, keyword: str, _filter: list, maximum_price: int) -> list:
        data = self.data_source.get_all_entries(keyword=keyword)
        filtered_data = self.__filter_irrelevant_entries(data=data, keyword=keyword, _filter=_filter)
        filtered_data = self.__filter_overpriced_entries(data=filtered_data, maximum_price=maximum_price)
        return filtered_data

    def find_anomalies(self) -> list:
        result = list()
        for query in self.queries:
            result.extend(self.__search(keyword=query.keyword, _filter=query.ignore, maximum_price=query.maximum_price))
        return result
