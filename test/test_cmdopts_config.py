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
        result, _ = cmdopts_config.separate_cmd_opts("")
        self.assertEqual(result, [])

    def test_separate_cmd_opts_whitespace_only(self):
        result, _ = cmdopts_config.separate_cmd_opts("   ")
        self.assertEqual(result, [])

    def test_separate_cmd_opts_words(self):
        result, _ = cmdopts_config.separate_cmd_opts("--host localhost --port 8080")
        self.assertEqual(result, ["--host", "localhost", "--port", "8080"])

    def test_separate_cmd_opts_quoted_words(self):
        result, _ = cmdopts_config.separate_cmd_opts(
            "--host 'local host' --name \"test value\""
        )
        self.assertEqual(result, ["--host", "local host", "--name", "test value"])

    def test_separate_cmd_opts_escaped_characters(self):
        result, _ = cmdopts_config.separate_cmd_opts(r"plain\ value escaped\"quote")
        self.assertEqual(result, ["plain value", 'escaped"quote'])

    def test_separate_cmd_opts_adjacent_quoted_and_unquoted_text(self):
        result, _ = cmdopts_config.separate_cmd_opts("prefix'quoted'\"text\"")
        self.assertEqual(
            result,
            ["prefixquotedtext"],
        )

    def test_separate_cmd_opts_unmatched_single_quote(self):
        result, warn_log = cmdopts_config.separate_cmd_opts("before 'unfinished value")
        self.assertEqual(result, ["before", "unfinished value"])
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(
            str(warn_log[0]), "clcoevt-cmdopts: No matching single quotation"
        )

    def test_separate_cmd_opts_unmatched_double_quote(self):
        result, warn_log = cmdopts_config.separate_cmd_opts('before "unfinished value')
        self.assertEqual(result, ["before", "unfinished value"])
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(
            str(warn_log[0]), "clcoevt-cmdopts: No matching double quotation"
        )

    def test_separate_cmd_opts_trailing_backslash(self):
        result, warn_log = cmdopts_config.separate_cmd_opts("before trailing\\")
        self.assertEqual(result, ["before", "trailing"])
        self.assertEqual(len(warn_log), 1)
        self.assertEqual(
            str(warn_log[0]), "clcoevt-cmdopts: No character follows the backslash"
        )

    def test_separate_cmd_opts_no_matching_backslash_in_double_quotes(self):
        result, warn_log = cmdopts_config.separate_cmd_opts(
            'before "unfinished value\\'
        )
        self.assertEqual(result, ["before", "unfinished value"])
        self.assertEqual(len(warn_log), 2)
        self.assertEqual(
            str(warn_log[0]), "clcoevt-cmdopts: No character follows the backslash"
        )
        self.assertEqual(
            str(warn_log[1]), "clcoevt-cmdopts: No matching double quotation"
        )

    def test_separate_cmd_opts_empty_quoted_values(self):
        result, _ = cmdopts_config.separate_cmd_opts("'' \"\"")
        self.assertEqual(result, ["", ""])

    def test_no_cmd_opts(self):
        del os.environ[self.cmd_opts]
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 0)

    def test_null(self):
        os.environ[self.cmd_opts] = ""
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 0)

    def test_string_1(self):
        os.environ[self.cmd_opts] = "--host=localhost"
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "localhost")

    def test_string_2(self):
        os.environ[self.cmd_opts] = "--host localhost"
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "localhost")

    def test_null_string(self):
        os.environ[self.cmd_opts] = "--host="
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["host"], "")

    def test_int_1(self):
        os.environ[self.cmd_opts] = "--port=12345"
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts["port"], 12345)

    def test_int_2(self):
        os.environ[self.cmd_opts] = "--port 12345"
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertEqual(opts["port"], 12345)

    def test_bool(self):
        os.environ[self.cmd_opts] = "--allow"
        opts, _ = cmdopts_config.cmdopts_get(self.settings)
        self.assertTrue(opts["allow"])

    def test_no_value_string(self):
        os.environ[self.cmd_opts] = "--host"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        for warning in warn_log:
            if str(warning) == "clcoevt-cmdopts: Invalid option: --host":
                break
        else:
            self.fail("Warning not found: clcoevt-cmdopts: Invalid option:")

    def test_invalid_type_int(self):
        os.environ[self.cmd_opts] = "--port=x"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        for warning in warn_log:
            if str(warning) == "clcoevt-cmdopts: Invalid value: --port=x":
                break
        else:
            self.fail("Warning not found: clcoevt-cmdopts: Invalid value:")

    def test_no_value_int(self):
        os.environ[self.cmd_opts] = "--port"
        _, warn_log = cmdopts_config.cmdopts_get(self.settings)
        for warning in warn_log:
            if str(warning) == "clcoevt-cmdopts: Invalid option: --port":
                break
        else:
            self.fail("Warning not found: clcoevt-cmdopts: Invalid option:")

    def test_no_cmdopts_setting(self):
        settings = types.ClcoevtCommandDetail(options=[])
        _, warn_log = cmdopts_config.cmdopts_get(settings)
        self.assertEqual(len(warn_log), 1)
        for warning in warn_log:
            if (
                str(warning)
                == "clcoevt-cmdopts: Not found: cmdopts.name in command_detail"
            ):
                break
        else:
            self.fail("Warning not found: clcoevt-cmdopts: Not found:")

    def test_no_cmdopts_envvar(self):
        settings = types.ClcoevtCommandDetail(
            cmdopts={
                "name": "TESTCMD_OPTS",
            },
            options=[],
        )
        del os.environ[self.cmd_opts]
        _, warn_log = cmdopts_config.cmdopts_get(settings)
        for warning in warn_log:
            if (
                str(warning)
                == "clcoevt-cmdopts: Environment variable not found: TESTCMD_OPTS"
            ):
                break
        else:
            self.fail(
                "Warning not found: clcoevt-cmdopts: Environment variable not found:"
            )
