import os
from .message import MessageInvalidValue, MessageNotFound, MessageInvalidSetting
from . import common


def get(options):
    values = common.C()
    messages = []
    for dest in options:
        option = options[dest]
        environmentVariableName = option.get("environmentVariable", None)
        option_type = option.get("type", None)
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
            messages.append(MessageInvalidSetting(option))
            continue
        if environmentVariableName not in os.environ:
            messages.append(MessageNotFound(environmentVariableName))
            continue
        value_string = os.environ[environmentVariableName]
        try:
            setattr(values, dest, convertor(value_string))
        except ValueError:
            messages.append(
                MessageInvalidValue(
                    environmentVariableName,
                    value_string,
                )
            )
    return values, messages
