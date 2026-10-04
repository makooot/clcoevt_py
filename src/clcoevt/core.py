from .cmdline_config import cmdline_get
from .cmdopts_config import cmdopts_get
from .envvar_config import envvar_get
from .tomlfile_config import tomlfile_get
from .types import ClcoevtCommandDetail, ClcoevtParserResult


class Clcoevt:
    def __init__(self, options: ClcoevtCommandDetail):
        values, unnamed = cmdline_get(options)
        self.cmdline = values
        self.args = unnamed
        self.warn_log: list[UserWarning] = []

        # TODO: skip if '--no-cmd-opts' is specified
        # TODO: set variable name if '--cmd-opts' is specified
        values, w = cmdopts_get(options)
        self.cmdopts = values
        self.warn_log.extend(w)

        # TODO: skip if '--no-env-var' is specified
        values, w = envvar_get(options.get("options", []))
        self.envvar = values
        self.warn_log.extend(w)

        # TODO: skip if '--no-toml-file' is specified
        try:
            options["toml"]["path"]
        except KeyError:
            self.warn_log.append(
                UserWarning("clcoevt-toml: Not found: toml.path in command_detail")
            )
        else:
            values, w = tomlfile_get(
                options["toml"]["path"],
                options.get("toml", {}).get("table", ""),
                options["options"],
            )
            self.tomlfile = values
            self.warn_log.extend(w)

        self.default: ClcoevtParserResult = {}
        for o in options.get("options", []):
            key = o.get("key", None)
            if key is None:
                continue
            default = o.get("default", None)
            if default is not None:
                self.default[key] = default
            else:
                self.warn_log.append(
                    UserWarning(f"clcoevt: No default value for option: {key}")
                )

    def get(self, key):
        try:
            return self.cmdline[key]
        except KeyError:
            pass

        try:
            return self.cmdopts[key]
        except KeyError:
            pass

        try:
            return self.envvar[key]
        except KeyError:
            pass

        try:
            return self.tomlfile[key]
        except KeyError:
            pass

        try:
            return self.default[key]
        except KeyError as e:
            raise e
