from typing import TypedDict, Any
from argparse import Action


class C:
    pass


# argparse settings
class ArgumentParserSetting(TypedDict, total=False):
    prog: str
    description: str | None
    usage: str | None
    epilog: str | None
    add_help: bool
    exit_on_error: bool
    suggest_on_error: bool


class AddArgumentSetting(TypedDict, total=False):
    dest: str | None
    default: str | int | bool | None
    action: str | type[Action]
    type: Any


# clcoevt command detail
class ClcoevtCommandArguments(TypedDict, total=False):
    key: str
    num: str | None


class ClcoevtCommand(TypedDict, total=False):
    name: str
    version: str
    usage: str
    arguments: list[ClcoevtCommandArguments]


class ClcoevtCmdopts(TypedDict, total=False):
    name: str


class ClcoevtToml(TypedDict, total=False):
    path: str


class ClcoevtCliOption(TypedDict, total=False):
    key: str
    type: str
    default: str | int | bool
    cmd: list[str]
    envvar: str | None
    toml: str | None


class ClcoevtCommandDetail(TypedDict, total=False):
    command: ClcoevtCommand
    cmdopts: ClcoevtCmdopts
    toml: ClcoevtToml
    options: list[ClcoevtCliOption]


# clcoevt command values
class ClcoevtCommandValues(TypedDict, total=False):
    cmdline: C
    cmdopts: C
    envvar: C
    tomlfile: C
    default: C
