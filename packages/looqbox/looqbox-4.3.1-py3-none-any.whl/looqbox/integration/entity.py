class Entity:
    def __init__(self, segment, text, value, name):
        self._segment = segment
        self._text = text,
        self._value = value
        self.name = name

    def as_sql_filter(self, column_name: str) -> str:

        filter_options = {
                          "$date": self._build_filter_for_temporal_field,
                          "$datetime": self._build_filter_for_temporal_field
                          }

        filter_method = filter_options.get(self.name, self._build_filter_for_atemporal_field)
        return filter_method(column_name)

    def _build_filter_for_temporal_field(self, column_name):
        return "\n".join(
            [f"AND {column_name}  between \"{date[0]}\" and \"{date[1]}\""
             for date in self._value]
        )

    def _build_filter_for_atemporal_field(self, column_name):

        if self._has_values_as_string() :
            filter_values = ", ".join([f"\"{query_filter}\"" for query_filter in self._value])
        else:
            filter_values = ", ".join([f"{query_filter}" for query_filter in self._value])

        return "\n".join(
            [f"AND {column_name}  in ({filter_values})"]
        )

    def _has_values_as_string(self) -> bool:
        types = [isinstance(value, str) for value in self._value]
        return any(types)



    @property
    def values(self):
        return self._value

    def to_dict(self):
        return {
            "segment": self._segment,
            "text": self._text,
            "values": self.values
        }
