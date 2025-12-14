import argparse
import os
from enum import Enum
from .message import MessageNotFound, MessageInvalidValueS, MessageInvalidType
from . import common


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


def get(env, options):
    values = common.C()
    messages = []

    if env not in os.environ:
        messages.append(MessageNotFound("Environment variable " + env))
        return values, messages

    argparse_setting = {}
    argparse_setting["prog"] = ""
    argparse_setting["usage"] = ""
    argparse_setting["description"] = ""
    argparse_setting["epilog"] = ""
    argparse_setting["add_help"] = False
    argparse_setting["exit_on_error"] = False
    argparse_setting["suggest_on_error"] = True
    parser = argparse.ArgumentParser(**argparse_setting)

    for dest in options:
        option = options[dest]
        name = option["cmd"]
        add_argument_setting = {}
        add_argument_setting["dest"] = dest
        add_argument_setting["default"] = None
        match option["type"]:
            case "bool":
                add_argument_setting["action"] = "store_true"
            case "string":
                add_argument_setting["action"] = "store"
            case "int":
                add_argument_setting["action"] = "store"
                add_argument_setting["type"] = int

        parser.add_argument(*name, **add_argument_setting)

    try:
        args = parser.parse_args(separate_cmd_opts(os.environ[env]))
    except argparse.ArgumentError as e:
        messages.append(MessageInvalidValueS(str(e)))
        return values, messages
    except argparse.ArgumentTypeError as e:
        messages.append(MessageInvalidType(str(e)))
        return values, messages

    for k, v in vars(args).items():
        if v is not None:
            setattr(values, k, v)

    return values, messages
