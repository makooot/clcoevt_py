import unittest
import sys
import os
import typing
import clcoevt.clcoevt as clcoevt
import clcoevt.types as types


class TestClcoevt(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.options = types.ClcoevtCommandDetail(
            command={
                "name": "testcmd",
                "version": "1.2.3",
                "usage": """\
                Usage: testcmd [options] [files...]
                """,
                "arguments": [
                    {"key": "file", "num": "0+"},
                ],
            },
            cmdopts={
                "name": "TESTCMD_OPTS",
            },
            toml={
                "path": "test-data/test_clcoevt.toml",
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

    def test_create_object(self):
        sys.argv = ["testcmd", "--host", "clihost", "--port", "14080", "--allow"]
        os.environ["TESTCMD_OPTS"] = "--host=cmdopthost --port=13080 --allow"
        os.environ["HOST"] = "envhost"
        os.environ["PORT"] = "12080"
        os.environ["ALLOW"] = "false"
        clco = clcoevt.Clcoevt(self.options)
        self.assertIsInstance(clco, clcoevt.Clcoevt)
        self.assertEqual(getattr(clco.default, "host"), "defaulthost")
        self.assertEqual(getattr(clco.default, "port"), 10080)
        self.assertEqual(getattr(clco.default, "allow"), False)
        self.assertEqual(getattr(clco.tomlfile, "host"), "tomlhost")
        self.assertEqual(getattr(clco.tomlfile, "port"), 11080)
        self.assertEqual(getattr(clco.tomlfile, "allow"), True)
        self.assertEqual(getattr(clco.envvar, "host"), "envhost")
        self.assertEqual(getattr(clco.envvar, "port"), 12080)
        self.assertEqual(getattr(clco.envvar, "allow"), False)
        self.assertEqual(getattr(clco.cmdopts, "host"), "cmdopthost")
        self.assertEqual(getattr(clco.cmdopts, "port"), 13080)
        self.assertEqual(getattr(clco.cmdopts, "allow"), True)
        self.assertEqual(getattr(clco.cmdline, "host"), "clihost")
        self.assertEqual(getattr(clco.cmdline, "port"), 14080)
        self.assertEqual(getattr(clco.cmdline, "allow"), True)

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
