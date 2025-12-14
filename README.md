# clcoevt_py
command options via commandline, environment variables and configuration files

## Example

```python
import clcoevt.clcoevt as clcoevt

command_details = {
    "command": {
        "name": "testcmd",
        "version": "1.2.3",
        "usage": """\
        Usage: testcmd [options] [files...]
        """,
        "arguments": {"file": {"num": "0+"}},
    },
    "cmdopts": {
        "name": "TESTCMD_OPTS",
    },
    "toml": {
        "path": "test-data/test_clcoevt.toml",
    },
    "options": {
        "host": {
            "type": "string",
            "default": "defaulthost",
            "cmd": ["--host"],
            "envvar": "HOST",
            "toml": "HOST",
        },
        "port": {
            "type": "int",
            "default": 10080,
            "cmd": ["--port"],
            "envvar": "PORT",
            "toml": "PORT",
        },
        "allow": {
            "type": "bool",
            "default": False,
            "cmd": ["-a", "--allow"],
            "envvar": "ALLOW",
            "toml": "ALLOW",
        },
    },
}

clco = clcoevt.Clcoevt(command_details)

host = clco.get("host")
port = clco.get("port")
allow = clco.get("allow")
files = clco.get("files")

print(f'host : {host}')
print(f'port : {port}')
print(f'allow: {allow}')
for i,f in enumerate(files):
    print(f'file[{i}]: {f}')
```
