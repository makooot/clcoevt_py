import os
from . import common
from .types import ClcoevtCliOption, ClcoevtParserResult


def get(
    options: list[ClcoevtCliOption],
) -> tuple[ClcoevtParserResult, list[UserWarning]]:
    values: ClcoevtParserResult = {}
    warn_log: list[UserWarning] = []

    for o in options:
        key = o["key"]
        environmentVariableName = o.get("envvar", None)
        option_type = o.get("type", None)
        match option_type:
            case "int":
                convertor = int
            case "string":
                convertor = str
            case "bool":
                convertor = common.str_to_bool
            case _:
                convertor = None
        if environmentVariableName is None or convertor is None:
            warn_log.append(UserWarning(f"Invalid setting: {o}"))
            continue
        if environmentVariableName not in os.environ:
            warn_log.append(
                UserWarning(
                    f"Environment variable not found: {environmentVariableName}"
                )
            )
            continue
        value_string = os.environ[environmentVariableName]
        try:
            values[key] = convertor(value_string)
        except ValueError:
            warn_log.append(
                UserWarning(
                    f"Invalid value for {environmentVariableName}: {value_string}"
                )
            )
    return values, warn_log
