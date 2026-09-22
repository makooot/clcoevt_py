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

        # TODO: skip if '--no-cmd-opts' is specified
        # TODO: set variable name if '--cmd-opts' is specified
        values, _ = cmdopts_get(options)
        self.cmdopts = values

        # TODO: skip if '--no-env-var' is specified
        values, _ = envvar_get(options["options"])
        self.envvar = values

        # TODO: skip if '--no-toml-file' is specified
        values, _ = tomlfile_get(
            options["toml"]["path"],
            options.get("toml", {}).get("table", ""),
            options["options"],
        )
        self.tomlfile = values

        self.default: ClcoevtParserResult = {}
        for o in options["options"]:
            key = o.get("key", None)
            if key is None:
                continue
            default = o.get("default", None)
            if default is not None:
                self.default[key] = default

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
