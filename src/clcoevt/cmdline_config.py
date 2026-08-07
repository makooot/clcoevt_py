import argparse
from . import common


def get(command, options):
    values = common.C()
    messages = []

    if "name" not in command:
        raise ValueError("name is required in command")
    if "version" not in command:
        raise ValueError("version is required in command")

    command_name = command.get("name", None)
    command_version = command.get("version", None)
    usage = command.get("usage", None)
    arguments = command.get("arguments", None)

    argparse_setting = {}
    argparse_setting["prog"] = command_name
    argparse_setting["usage"] = usage
    argparse_setting["description"] = None
    argparse_setting["epilog"] = None
    argparse_setting["add_help"] = False
    parser = argparse.ArgumentParser(**argparse_setting)

    parser.add_argument("-h", "--help", action="help")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + command_version
    )

    if options is not None:
        for o in options:
            key = o.get("key", None)
            name = o.get("cmd", None)
            if name is None:
                continue
            opt_type = o.get("type", None)
            add_argument_setting = {}
            add_argument_setting["dest"] = key
            add_argument_setting["default"] = None
            match opt_type:
                case "bool":
                    add_argument_setting["action"] = "store_true"
                case "string":
                    add_argument_setting["action"] = "store"
                case "int":
                    add_argument_setting["action"] = "store"
                    add_argument_setting["type"] = int
                case _:
                    raise ValueError("Invalid option type: " + str(opt_type))

            parser.add_argument(*name, **add_argument_setting)

    if arguments is not None:
        for a in arguments:
            key = a.get("key", None)
            if key is None:
                continue
            num = a.get("num", None)
            if num is None:
                continue
            match num:
                case "1":
                    parser.add_argument(key, nargs=1)
                case "0+":
                    parser.add_argument(key, nargs="*")
                case "1+":
                    parser.add_argument(key, nargs="+")
                case "0-1":
                    parser.add_argument(key, nargs="?")
                case _:
                    raise ValueError("Invalid argument num: " + str(num))

    args = parser.parse_args()
    for k, v in vars(args).items():
        if v is not None:
            setattr(values, k, v)
    return values, messages
