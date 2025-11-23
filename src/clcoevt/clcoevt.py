from . import cmdline_config
from . import cmdopts_config
from . import envvar_config
from . import tomlfile_config
from . import common


class Clcoevt:
    def __init__(self, options):
        values, messages = cmdline_config.get(options)
        self.cmdline = values

        # TODO: skip if '--no-cmd-opts' is specified
        # TODO: set variable name if '--cmd-opts' is specified
        values, messages = cmdopts_config.get(options["cmd_opts"], options["option"])
        self.cmdopts = values

        # TODO: skip if '--no-env-var' is specified
        values, messages = envvar_config.get(options["option"])
        self.envvar = values

        # TODO: skip if '--no-toml-file' is specified
        values, messages = tomlfile_config.get(options["toml_file"], options["option"])
        self.tomlfile = values

        self.default = common.C()
        for dest in options["option"]:
            default = options["option"][dest].get("default", None)
            if default is not None:
                setattr(self.default, dest, default)

    def get(self, key):
        try:
            return getattr(self.cmdline, key)
        except AttributeError:
            pass

        try:
            return getattr(self.cmdopts, key)
        except AttributeError:
            pass

        try:
            return getattr(self.envvar, key)
        except AttributeError:
            pass

        try:
            return getattr(self.tomlfile, key)
        except AttributeError:
            pass

        try:
            return getattr(self.default, key)
        except AttributeError as e:
            raise e
