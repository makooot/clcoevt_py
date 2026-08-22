import argparse
from . import types


def get(command: types.ClcoevtCommand, options: list[types.ClcoevtCliOption]):
    values = types.C()
    messages = []

    if "name" not in command:
        raise ValueError("name is required in command")
    if "version" not in command:
        raise ValueError("version is required in command")

    command_name: str = command.get("name", "")
    command_version: str = command.get("version", "")
    usage: str = command.get("usage", "")
    arguments: list[types.ClcoevtCommandArguments] | None = command.get(
        "arguments", None
    )

    argparse_setting = types.ArgumentParserSetting(
        prog=command_name,
        usage=usage,
        add_help=False,
        description=None,
        epilog=None,
    )
    parser = argparse.ArgumentParser(**argparse_setting)

    parser.add_argument("-h", "--help", action="help")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + command_version
    )

    if options is not None:
        for o in options:
            key: str | None = o.get("key", None)
            name: list[str] | None = o.get("cmd", None)
            if name is None:
                continue
            opt_type: str | None = o.get("type", None)
            add_argument_setting = types.AddArgumentSetting(
                dest=key,
                default=None,
            )
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
