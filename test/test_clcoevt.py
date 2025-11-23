import unittest
import sys
import os
import clcoevt.clcoevt as clcoevt


class TestClcoevt(unittest.TestCase):
    def setUp(self):
        self.options = {
            "command_name": "testcmd",
            "command_version": "1.2.3",
            "usage": """\
                Usage: testcmd [options] [files...]
                """,
            "argument": {"file": {"num": "0+"}},
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
        self.assertEqual(clco.default.host, "defaulthost")
        self.assertEqual(clco.default.port, 10080)
        self.assertEqual(clco.default.allow, False)
        self.assertEqual(clco.tomlfile.host, "tomlhost")
        self.assertEqual(clco.tomlfile.port, 11080)
        self.assertEqual(clco.tomlfile.allow, True)
        self.assertEqual(clco.envvar.host, "envhost")
        self.assertEqual(clco.envvar.port, 12080)
        self.assertEqual(clco.envvar.allow, False)
        self.assertEqual(clco.cmdopts.host, "cmdopthost")
        self.assertEqual(clco.cmdopts.port, 13080)
        self.assertEqual(clco.cmdopts.allow, True)
        self.assertEqual(clco.cmdline.host, "clihost")
        self.assertEqual(clco.cmdline.port, 14080)
        self.assertEqual(clco.cmdline.allow, True)

    def test_default_values(self):
        sys.argv = ["testcmd"]
        del os.environ["TESTCMD_OPTS"]
        del os.environ["HOST"]
        del os.environ["PORT"]
        del os.environ["ALLOW"]
        self.options["toml_file"] = "file-not-found.toml"
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
