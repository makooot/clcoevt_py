import unittest
import os
import typing
import clcoevt.cmdopts_config as cmdopts_config
import clcoevt.types as types


class TestCmdsOptsConfig(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.settings = types.ClcoevtCommandDetail(
            cmdopts={
                "name": "TESTCMD_OPTS",
            },
            options=[
                {
                    "key": "host",
                    "cmd": ["--host"],
                    "type": "string",
                },
                {
                    "key": "port",
                    "cmd": ["--port"],
                    "type": "int",
                },
                {
                    "key": "allow",
                    "cmd": ["--allow"],
                    "type": "bool",
                },
            ],
        )

        self.cmd_opts = "TESTCMD_OPTS"
        os.environ[self.cmd_opts] = ""

    def test_no_cmd_opts(self):
        del os.environ[self.cmd_opts]
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 0)
        self.assertEqual(len(warn_log), 0)

    def test_null(self):
        os.environ[self.cmd_opts] = ""
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 0)
        self.assertEqual(len(warn_log), 0)

    def test_string_1(self):
        os.environ[self.cmd_opts] = "--host=localhost"
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "localhost")
        self.assertEqual(len(warn_log), 0)

    def test_string_2(self):
        os.environ[self.cmd_opts] = "--host localhost"
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "localhost")
        self.assertEqual(len(warn_log), 0)

    def test_null_string(self):
        os.environ[self.cmd_opts] = "--host="
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "")
        self.assertEqual(len(warn_log), 0)

    def test_int_1(self):
        os.environ[self.cmd_opts] = "--port=12345"
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["port"], 12345)
        self.assertEqual(len(warn_log), 0)

    def test_int_2(self):
        os.environ[self.cmd_opts] = "--port 12345"
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(opts["port"], 12345)
        self.assertEqual(len(warn_log), 0)

    def test_bool(self):
        os.environ[self.cmd_opts] = "--allow"
        opts, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertTrue(opts["allow"])
        self.assertEqual(len(warn_log), 0)

    def test_no_value_string(self):
        os.environ[self.cmd_opts] = "--host"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(str(warn_log[0]), "Invalid option: --host")

    def test_invalid_type_int(self):
        os.environ[self.cmd_opts] = "--port=x"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(str(warn_log[0]), "Invalid value: --port=x")

    def test_no_value_int(self):
        os.environ[self.cmd_opts] = "--port"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(str(warn_log[0]), "Invalid option: --port")
