from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.base_parameter import _BaseParameter
from roocs_utils.parameter.param_utils import time_components, string_to_dict


class TimeComponentsParameter(_BaseParameter):
    """
    Class for time components parameter used in subsetting operation.

    The Time Components are any, or none of:
      - year: [list of years]
      - month: [list of months]
      - day: [list of days]
      - hour: [list of hours]
      - minute: [list of minutes]
      - second: [list of seconds]

    `month` is special: you can use either strings or values:
       "feb", "mar" == 2, 3 == "02,03"

    Validates the times input and parses them into a dictionary.
    """

    allowed_input_types = [dict, str, time_components, type(None)]

    def _parse(self):
        try:
            if self.input in (None, ""):
                return None
            elif isinstance(self.input, time_components):
                return self.input.value
            elif isinstance(self.input, str):
                time_comp_dict = string_to_dict(self.input, splitters=("|", ":", ","))
                return time_components(**time_comp_dict).value
            else:  # Must be a dict to get here
                return time_components(**self.input).value
        except Exception:
            raise InvalidParameterValue(
                f"Cannot create TimeComponentsParameter " f"from: {self.input}"
            )

    def asdict(self):
        # Just return the value, either a dict or None
        return {"time_components": self.value}

    def __str__(self):
        if self.value is None:
            return "No time components specified"

        resp = "Time components to select:"
        for key, value in self.value.items():
            resp += f"\n    {key} => {value}"
        return resp
