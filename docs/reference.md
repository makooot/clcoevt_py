# Configuration format

The root object is a dictionary passed to `Clcoevt`.

```python
command_detail = {
    "cmdline": {
        # optional: help/version option names
        # "help_option": ["-h", "--help"],
        # "version_option": ["-v", "--version"],
    },
    "cmdopts": {
        # optional: environment variable name that contains extra command-line arguments
        "name": "MYAPP_OPTS",
    },
    "toml": {
        # required if you want to read a TOML file
        "path": "config.toml",
    },
    "options": [
        {
            "key": "host",
            "type": "string",
            "default": "localhost",
            "cmd": ["--host"],
            "envvar": "HOST",
            "toml": "HOST",
        },
        {
            "key": "port",
            "type": "int",
            "default": 8080,
            "cmd": ["--port"],
            "envvar": "PORT",
            "toml": "PORT",
        },
        {
            "key": "allow",
            "type": "bool",
            "default": False,
            "cmd": ["--allow"],
            "envvar": "ALLOW",
            "toml": "ALLOW",
        },
    ],
}
```

### Option fields

Each item in `options` can include the following keys:

- `key`: option key used in `clco.get("...")`
- `type`: data type; supported values are `string`, `int`, and `bool`
- `default`: fallback value when none of the other sources provide a value
- `cmd`: command-line flags for the option such as `"--host"`, `"-p"`, or `"--port"`
- `envvar`: environment variable name to read from `os.environ`
- `toml`: TOML key name to read from the TOML file

## Supported value types

### string

```python
{
    "key": "host",
    "type": "string",
    "cmd": ["--host"],
    "envvar": "HOST",
    "toml": "HOST",
}
```

Examples:

- command line: `--host example.com`
- env var: `HOST=example.com`
- TOML: `HOST = "example.com"`

### int

```python
{
    "key": "port",
    "type": "int",
    "cmd": ["--port"],
    "envvar": "PORT",
    "toml": "PORT",
}
```

Examples:

- command line: `--port 8080`
- env var: `PORT=8080`
- TOML: `PORT = 8080`

### bool

```python
{
    "key": "allow",
    "type": "bool",
    "cmd": ["--allow"],
    "envvar": "ALLOW",
    "toml": "ALLOW",
}
```

Examples:

- command line: `--allow`
- env var: `ALLOW=true`
- TOML: `ALLOW = true`

Boolean values are accepted in common truthy/falsy forms such as `true`,
`false`, `yes`, `no`, `on`, `off`, `y`, `n`, `t`, and `f`.

## Command options from an environment variable

You can pass extra arguments through an environment variable by setting
`cmdopts.name`.

```python
command_detail = {
    "cmdopts": {
        "name": "MYAPP_OPTS",
    },
    "options": [
        {"key": "host", "type": "string", "cmd": ["--host"]},
        {"key": "port", "type": "int", "cmd": ["--port"]},
    ],
}
```

Then:

```bash
export MYAPP_OPTS="--host=example.com --port 8080"
```

Those arguments are parsed as if they were passed on the real command line.

## TOML file support

If the `toml.path` entry is set, the library opens the file and reads the
matching keys.

Example TOML:

```toml
HOST = "localhost"
PORT = 8080
ALLOW = true
```

```python
command_detail = {
    "toml": {"path": "config.toml"},
    "options": [
        {"key": "host", "type": "string", "toml": "HOST"},
        {"key": "port", "type": "int", "toml": "PORT"},
        {"key": "allow", "type": "bool", "toml": "ALLOW"},
    ],
}
```

# Accessing resolved values

```python
clco = clcoevt.Clcoevt(command_detail)

clco.get("host")
# get() resolves in priority order:
# 1. command line arguments
# 2. environment variable configured by `cmdopts`
# 3. environment variables
# 4. TOML file
# 5. default values

clco.args
# args contains positional arguments not captured by option definitions.
```

# Exceptions

The library raises these exceptions when parsing fails.

`ClcoevtShowHelpException`: `-h`, `--help`, or the specified help option appears.

`ClcoevtShowVersionException`: `--version` or the specified version option appears.

`ClcoevtValueError`: invalid type, invalid option format, or invalid value.

# Notes
command line arguments and environment variable configured by `cmdopts` are
processed with the same option definitions.

This library is helpful when you want a single configuration object that
can combine command line flags, environment values, and a TOML file with
predictable precedence.
