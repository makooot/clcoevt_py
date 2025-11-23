# clcoevt_py
command options via commandline, environment variables and configuration files

## Example

```python
import clcoevt.clcoevt as clcoevt

command_details = {
    "command_name": "testcmd",
    "command_version": "0.1.0",
    "usage": """\
        Usage: testcmd [options] [files...]
        """,
    "argument": {"files": {"num": "0+"}},
    "cmd_opts": "TESTCMD_OPTS",
    "toml_file": "test-data/test_clcoevt.toml",
    "option": {
        "host": {
            "type": "string",
            "default": "defaulthost",
            "cmds": ["--host"],
            "environmentVariable": "HOST",
            "toml": "HOST",
        },
        "port": {
            "type": "int",
            "default": 10080,
            "cmds": ["--port"],
            "environmentVariable": "PORT",
            "toml": "PORT",
        },
        "allow": {
            "type": "bool",
            "default": False,
            "cmds": ["-a", "--allow"],
            "environmentVariable": "ALLOW",
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
