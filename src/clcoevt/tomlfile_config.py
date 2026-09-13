import tomllib
from .types import ClcoevtCliOption, ClcoevtParserResult


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


def tomlfile_get(
    filename: str, options: list[ClcoevtCliOption]
) -> tuple[ClcoevtParserResult, list[UserWarning]]:
    values: ClcoevtParserResult = {}
    warn_log: list[UserWarning] = []
    try:
        with open(filename, "rb") as f:
            tomlobj = tomllib.load(f)
    except FileNotFoundError:
        warn_log.append(UserWarning(f"File not found: {filename}"))
        return values, warn_log
    except tomllib.TOMLDecodeError:
        warn_log.append(UserWarning(f"Invalid TOML file: {filename}"))
        return values, warn_log
    return tomlfile_geto(values, warn_log, tomlobj, options)


def tomlfile_geto(
    values: ClcoevtParserResult,
    warn_log: list[UserWarning],
    tomlobj,
    options: list[ClcoevtCliOption],
) -> tuple[ClcoevtParserResult, list[UserWarning]]:
    for o in options:
        key = o["key"]
        name = o["toml"]
        value_type = o["type"]
        match value_type:
            case "int":
                convertor = thru_int
            case "string":
                convertor = thru_str
            case "bool":
                convertor = thru_bool
            case _:
                convertor = None
        if name is None or convertor is None or key is None:
            warn_log.append(UserWarning(f"Invalid setting: {o}"))
            continue
        if name in tomlobj:
            try:
                values[key] = convertor(tomlobj[name])
            except ValueError:
                warn_log.append(
                    UserWarning(f"Invalid value for {name}: {tomlobj[name]}")
                )

    return values, warn_log
