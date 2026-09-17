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

    def test_separate_cmd_opts_empty_string(self):
        self.assertEqual(cmdopts_config.separate_cmd_opts(""), [])

    def test_separate_cmd_opts_whitespace_only(self):
        self.assertEqual(cmdopts_config.separate_cmd_opts("   "), [])

    def test_separate_cmd_opts_words(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts("--host localhost --port 8080"),
            ["--host", "localhost", "--port", "8080"],
        )

    def test_separate_cmd_opts_quoted_words(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts(
                "--host 'local host' --name \"test value\""
            ),
            ["--host", "local host", "--name", "test value"],
        )

    def test_separate_cmd_opts_escaped_characters(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts(r"plain\ value escaped\"quote"),
            ["plain value", 'escaped"quote'],
        )

    def test_separate_cmd_opts_adjacent_quoted_and_unquoted_text(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts("prefix'quoted'\"text\""),
            ["prefixquotedtext"],
        )

    def test_separate_cmd_opts_unmatched_single_quote(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts("before 'unfinished value"),
            ["before", "unfinished value"],
        )

    def test_separate_cmd_opts_unmatched_double_quote(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts('before "unfinished value'),
            ["before", "unfinished value"],
        )

    def test_separate_cmd_opts_trailing_backslash(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts("before trailing\\"),
            ["before", "trailing"],
        )

    def test_separate_cmd_opts_empty_quoted_values(self):
        self.assertEqual(
            cmdopts_config.separate_cmd_opts("'' \"\""),
            ["", ""],
        )

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
