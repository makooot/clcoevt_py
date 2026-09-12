from typing import TypedDict


class C:
    pass


# clcoevt command detail
class ClcoevtCmdline(TypedDict, total=False):
    help_option: list[str]
    version_option: list[str]


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
    options: list[ClcoevtCliOption]
    cmdline: ClcoevtCmdline
    cmdopts: ClcoevtCmdopts
    toml: ClcoevtToml


# clcoevt command values
type ClcoevtParserResult = dict[str, str | int | bool | None | list[str]]


class ClcoevtCommandValues(TypedDict, total=False):
    cmdline: ClcoevtParserResult
    cmdopts: ClcoevtParserResult
    envvar: C
    tomlfile: C
    default: C


class ClcoevtShowHelpException(Exception):
    pass


class ClcoevtShowVersionException(Exception):
    pass


class ClcoevtValueError(Exception):
    pass
