import os
from enum import Enum
from fruits_skewers.skewer import skewer_parser
from fruits_skewers.types import (
    SkewerOption,
    SkewerCommandDetail,
    SkewerValueError,
)
from .types import ClcoevtCommandDetail, ClcoevtValueError, ClcoevtParserResult


def separate_cmd_opts(s):
    class Status(Enum):
        SEPARATOR = 0
        NON_QUOTE = 1
        IN_SINGLE_QUOTE = 2
        IN_DOUBLE_QUOTE = 3
        BACKSLASH = 4
        BACKSLASH_IN_DOUBLE_QUOTE = 5

    result = []
    token = ""
    token_exist = False
    status = Status.SEPARATOR
    for c in list(s):
        match status:
            case Status.SEPARATOR:
                match c:
                    case " ":
                        pass
                    case "\\":
                        token_exist = True
                        status = Status.BACKSLASH
                    case "'":
                        token_exist = True
                        status = Status.IN_SINGLE_QUOTE
                    case '"':
                        token_exist = True
                        status = Status.IN_DOUBLE_QUOTE
                    case _:
                        token = token + c
                        token_exist = True
                        status = Status.NON_QUOTE
            case Status.NON_QUOTE:
                match c:
                    case " ":
                        if token_exist:
                            result.append(token)
                        token = ""
                        token_exist = False
                        status = Status.SEPARATOR
                    case "\\":
                        status = Status.BACKSLASH
                    case "'":
                        status = Status.IN_SINGLE_QUOTE
                    case '"':
                        status = Status.IN_DOUBLE_QUOTE
                    case _:
                        token = token + c
            case Status.IN_SINGLE_QUOTE:
                match c:
                    case "'":
                        status = Status.NON_QUOTE
                    case _:
                        token = token + c
            case Status.IN_DOUBLE_QUOTE:
                match c:
                    case "\\":
                        status = Status.BACKSLASH_IN_DOUBLE_QUOTE
                    case '"':
                        status = Status.NON_QUOTE
                    case _:
                        token = token + c
                        status = Status.IN_DOUBLE_QUOTE
            case Status.BACKSLASH:
                token = token + c
                status = Status.NON_QUOTE
            case Status.BACKSLASH_IN_DOUBLE_QUOTE:
                token = token + c
                status = Status.IN_DOUBLE_QUOTE
    match status:
        case Status.SEPARATOR:
            pass
        case Status.NON_QUOTE:
            if token_exist:
                result.append(token)
        case Status.IN_SINGLE_QUOTE:
            # TODO: warning: No matching single quotation
            if token_exist:
                result.append(token)
        case Status.IN_DOUBLE_QUOTE:
            # TODO: warning: No matching double quotation
            if token_exist:
                result.append(token)
        case Status.BACKSLASH:
            # TODO: warning: No character follows the backslash
            if token_exist:
                result.append(token)
        case Status.BACKSLASH_IN_DOUBLE_QUOTE:
            # TODO: warning: No character follows the backslash
            # TODO: warning: No matching double quotation
            if token_exist:
                result.append(token)
    return result


def cmdopts_get(
    command_detail: ClcoevtCommandDetail,
) -> tuple[ClcoevtParserResult, list[UserWarning]]:
    values: ClcoevtParserResult = {}
    warn_log: list[UserWarning] = []

    try:
        env = command_detail["cmdopts"]["name"]
    except KeyError:
        raise ClcoevtValueError("Not found: cmdopts.name in command_detail")

    if env not in os.environ:
        return values, warn_log

    args = separate_cmd_opts(os.environ[env])
    skewer_command_detail: SkewerCommandDetail = {
        "cmdline": {
            "help_option": [],
            "version_option": [],
        },
        "options": [],
    }
    for o in command_detail.get("options", []):
        key = o.get("key", None)
        if key is None:
            continue
        cmd = o.get("cmd", [])
        if len(cmd) == 0:
            continue
        skewer_option: SkewerOption = {
            "key": key,
            "type": o.get("type", "string"),
            "cmd": cmd,
        }
        skewer_command_detail["options"].append(skewer_option)

    try:
        values, _ = skewer_parser(skewer_command_detail, args)
    except SkewerValueError as e:
        warn_log.append(UserWarning(e.args[0]))

    return values, warn_log
