import fruits_skewers

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
    skewer_command_detail: fruits_skewers.SkewerCommandDetail = {
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
        skewer_option: fruits_skewers.SkewerOption = {
            "key": key,
            "type": o.get("type", "string"),
            "cmd": cmd,
        }
        skewer_command_detail["options"].append(skewer_option)

    try:
        values, unnamed = fruits_skewers.skewer_parser(skewer_command_detail, args)
    except fruits_skewers.SkewerShowHelpException:
        raise ClcoevtShowHelpException()
    except fruits_skewers.SkewerShowVersionException:
        raise ClcoevtShowVersionException()
    except fruits_skewers.SkewerValueError as e:
        raise ClcoevtValueError(f"clcoevt-cmdline: {e.args[0]}")
    return values, unnamed
