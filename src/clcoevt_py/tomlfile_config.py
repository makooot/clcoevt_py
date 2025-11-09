import tomllib
from .message import (
    MessageFileNotFound,
    MessageInvalidTomlFile,
    MessageInvalidTomlValue,
    MessageInvalidSetting,
)
from . import common


def thru_str(value):
    if isinstance(value, str):
        return value
    raise ValueError


def thru_int(value):
    if type(value) is int:
        return value
    raise ValueError


def thru_bool(value):
    if isinstance(value, bool):
        return value
    raise ValueError


def get(filename, options):
    values = common.C()
    messages = []
    try:
        with open(filename, "rb") as f:
            tomlobj = tomllib.load(f)
    except FileNotFoundError:
        messages.append(MessageFileNotFound(filename))
        return values, messages
    except tomllib.TOMLDecodeError:
        messages.append(MessageInvalidTomlFile(filename))
        return values, messages
    return _geto(values, messages, tomlobj, options)


def _geto(values, messages, tomlobj, options):
    for dest in options:
        option = options[dest]
        name = option.get("toml", None)
        value_type = option.get("type", None)
        match value_type:
            case "int":
                convertor = thru_int
            case "string":
                convertor = thru_str
            case "bool":
                convertor = thru_bool
            case _:
                convertor = None
        if name is None or convertor is None or dest is None:
            messages.append(MessageInvalidSetting(option))
            continue
        if name in tomlobj:
            try:
                setattr(values, dest, convertor(tomlobj[name]))
            except ValueError:
                messages.append(MessageInvalidTomlValue(name, tomlobj[name]))

    return values, messages
