from ..search_field import SearchField
from ..search_operator import SearchOperator


class AdvancedSearchOption:
    def __init__(
        self,
        search_operator: SearchOperator,
        search_field: SearchField,
        search_value: str,
    ):
        self._search_operator = search_operator
        self._search_field = search_field
        self._search_value = search_value

    @property
    def search_operator(self):
        return self._search_operator

    @property
    def search_field(self):
        return self._search_field

    @property
    def search_value(self):
        return self._search_value
