from fruits_skewers.skewer import skewer_parser
from fruits_skewers.types import (
    SkewerOption,
    SkewerCommandDetail,
    SkewerShowHelpException,
    SkewerShowVersionException,
    SkewerValueError,
)
from .types import (
    ClcoevtCommandDetail,
    ClcoevtParserResult,
    ClcoevtShowHelpException,
    ClcoevtShowVersionException,
    ClcoevtValueError,
)


def cmdline_get(
    command_detail: ClcoevtCommandDetail, args: list[str] | None = None
) -> tuple[ClcoevtParserResult, list[str]]:
    skewer_command_detail: SkewerCommandDetail = {
        "cmdline": command_detail.get("cmdline", {}),
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
        values, unnamed = skewer_parser(skewer_command_detail, args)
    except SkewerShowHelpException:
        raise ClcoevtShowHelpException()
    except SkewerShowVersionException:
        raise ClcoevtShowVersionException()
    except SkewerValueError as e:
        raise ClcoevtValueError(e.args[0])
    return values, unnamed
