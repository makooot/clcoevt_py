import unittest
import sys
import os
import typing
#import clcoevt.core as clcoevt
#import clcoevt.types as types
import clcoevt


class TestPackage(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.options = clcoevt.ClcoevtCommandDetail(
            cmdline={},
            cmdopts={
                "name": "TESTCMD_OPTS",
            },
            toml={
                "path": "test-data/test-package.toml",
            },
            options=[
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
        )

        os.environ["TESTCMD_OPTS"] = ""
        os.environ["HOST"] = ""
        os.environ["PORT"] = "0"
        os.environ["ALLOW"] = "true"

    def test_default_values(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        del os.environ["HOST"]
        del os.environ["PORT"]
        del os.environ["ALLOW"]
        self.options["toml"]["path"] = "file-not-found.toml"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "defaulthost")
        self.assertEqual(clco.get("port"), 10080)
        self.assertEqual(clco.get("allow"), False)

    def test_toml_file(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        del os.environ["HOST"]
        del os.environ["PORT"]
        del os.environ["ALLOW"]
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "tomlhost")
        self.assertEqual(clco.get("port"), 11080)
        self.assertEqual(clco.get("allow"), True)

    def test_env_variables(self):
        sys.argv = ["testcmd"]
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "12080"
        os.environ["ALLOW"] = "false"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "envhost")
        self.assertEqual(clco.get("port"), 12080)
        self.assertEqual(clco.get("allow"), False)

    def test_cmdopt_variables(self):
        sys.argv = ["testcmd"]
        os.environ["TESTCMD_OPTS"] = "--host=cmdopthost --port=13080 --allow"
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "12080"
        os.environ["ALLOW"] = "false"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "cmdopthost")
        self.assertEqual(clco.get("port"), 13080)
        self.assertEqual(clco.get("allow"), True)

    def test_command_line_arguments(self):
        sys.argv = ["testcmd", "--host", "clihost", "--port", "14080", "--allow"]
        os.environ["TESTCMD_OPTS"] = "--host=cmdopthost --port=13080"
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "12080"
        os.environ["ALLOW"] = "false"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "clihost")
        self.assertEqual(clco.get("port"), 14080)
        self.assertEqual(clco.get("allow"), True)

    def test_empty_command_line_arguments(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        del os.environ["HOST"]
        del os.environ["PORT"]
        del os.environ["ALLOW"]
        self.options["toml"]["path"] = "file-not-found.toml"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.args, [])
        self.assertEqual(clco.get("host"), "defaulthost")

    def test_command_line_help_exception(self):
        sys.argv = ["testcmd", "--help"]
        with self.assertRaises(clcoevt.ClcoevtShowHelpException):
            clcoevt.Clcoevt(self.options)

    def test_command_line_version_exception(self):
        sys.argv = ["testcmd", "--version"]
        with self.assertRaises(clcoevt.ClcoevtShowVersionException):
            clcoevt.Clcoevt(self.options)

    def test_invalid_command_line_value(self):
        sys.argv = ["testcmd", "--port", "not-an-integer"]
        with self.assertRaises(clcoevt.ClcoevtValueError):
            clcoevt.Clcoevt(self.options)

    def test_invalid_environment_value_falls_back(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "not-an-integer"
        os.environ["ALLOW"] = "not-a-bool"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "envhost")
        self.assertEqual(clco.get("port"), 11080)
        self.assertEqual(clco.get("allow"), True)

    def test_empty_and_zero_values(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        os.environ["HOST"] = ""
        os.environ["PORT"] = "0"
        os.environ["ALLOW"] = "false"
        self.options["toml"]["path"] = "file-not-found.toml"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("host"), "")
        self.assertEqual(clco.get("port"), 0)
        self.assertEqual(clco.get("allow"), False)

    def test_negative_integer_value(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "-1"
        os.environ["ALLOW"] = "false"
        self.options["toml"]["path"] = "file-not-found.toml"
        clco = clcoevt.Clcoevt(self.options)
        self.assertEqual(clco.get("port"), -1)

    def test_unknown_key(self):
        sys.argv = ["testcmd"]
        clco = clcoevt.Clcoevt(self.options)
        with self.assertRaises(KeyError):
            clco.get("unknown")
