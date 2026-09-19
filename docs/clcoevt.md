# clcoevt
`clcoevt` is a small configuration library that resolves option values
from multiple sources and returns the value with the highest priority.

## overview

The library reads values in this order:

1. command line arguments
2. environment variable configured by `cmdopts`
3. environment variables
4. TOML file
5. default values

This makes it easy to layer configuration while keeping a clear precedence
model.

## Installation

```bash
pip install git+https://github.com/makooot/clcoevt_py.git
```

## Usage

```python
import sys

import clcoevt

command_detail: clcoevt.ClcoevtCommandDetail = {
    "cmdline": {},
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
    clco = clcoevt.Clcoevt(command_detail)
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

print(f"host: {host}")
print(f"port: {port}")
print(f"allow: {allow}")
for i, arg in enumerate(args):
    print(f"args[{i}]: {arg}")
```

When you run:

```bash
export HOST=prod-host
export PORT=8080
export ALLOW=false
export TESTCMD_OPTS="--host=cmd-host --port=9000 --allow"
python app.py --host cli-host --port 7000 --allow
```

`clco.get("host")` resolves to `cli-host` because command line arguments take
priority over all other sources.
