# clcoevt_py
command options via commandline, environment variables and configuration files

# Installation

```bash
pip install clcoevt
```

## Quick Start

Here is a simple example of how to use the library:

```python
import sys

import clcoevt


command_details:clcoevt.ClcoevtCommanDetail = {
    "cmdline": {
    },
    "cmdopts": {
        "name": "TESTCMD_OPTS",
    },
    "toml": {
        "path": "test-data/test_clcoevt.toml",
    },
    "options": [
        {
            "key": "host",
            "type": "string",
            "default": "defaulthost",
            "cmd": ["--host"],
            "envvar": "HOST",
            "toml": "HOST",
        },
        {
            "key": "port",
            "type": "int",
            "default": 10080,
            "cmd": ["--port"],
            "envvar": "PORT",
            "toml": "PORT",
        },
        {
            "key": "allow",
            "type": "bool",
            "default": False,
            "cmd": ["-a", "--allow"],
            "envvar": "ALLOW",
            "toml": "ALLOW",
        },
    ],
}

try:
    clco = clcoevt.Clcoevt(command_details)
except clcoevt.ClcoevtShowVersionException:
    print("CMD 0.0.0")
    sys.exit(0)
except clcoevt.ClcoevtShowHelpException:
    print("CMD OPTIONS")
    sys.exit(0)
except clcoevt.ClcoevtValueError as e:
    print(e)
    sys.exit(1)

host = clco.get("host")
port = clco.get("port")
allow = clco.get("allow")
args = clco.args

print(f'host : {host}')
print(f'port : {port}')
print(f'allow: {allow}')
for i,a in enumerate(args):
    print(f'args[{i}]: {a}')
exit(0)
```

## Contributing

Please refer to CONTRIBUTING.md for details on how this repository handles
issues, pull requests, and forks.

## License

MIT License
