import unittest
import sys
import clcoevt.cmdline_config as cmdline_config


class TestEnvvarConfig(unittest.TestCase):
    def setUp(self):
        self.options = {
            "command_name": "testcmd",
            "command_version": "1.2.3",
            "argument": {
                "file": {"num": "0+"},
            },
            "option": {
                "host": {"cmds": ["--host"], "type": "string"},
                "port": {"cmds": ["--port"], "type": "int"},
                "allow": {"cmds": ["--allow"], "type": "bool"},
            },
        }

    def test_invalid_setting_no_command_name(self):
        options = {}
        with self.assertRaises(ValueError):
            cmdline_config.get(options)

    def test_invalid_setting_no_command_version(self):
        options = {"command_name": "testcmd"}
        with self.assertRaises(ValueError):
            cmdline_config.get(options)

    def test_invalid_setting_unsuported_option_type(self):
        options = {
            "command_name": "testcmd",
            "command_version": "1.2.3",
            "option": {"opt1": {"cmds": ["--opt1"], "type": "unsuported_type"}},
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(options)

    def test_invalid_setting_invalid_argument_num(self):
        options = {
            "command_name": "testcmd",
            "command_version": "1.2.3",
            "argument": {"arg1": {"num": "invalid_num"}},
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(options)

    def test_no_arguments(self):
        sys.argv = ["testcmd"]
        values, messages = cmdline_config.get(self.options)
        self.assertFalse(hasattr(values, "host"))
        self.assertFalse(hasattr(values, "port"))
        self.assertFalse(hasattr(values, "allow"))
        self.assertEqual(values.file, [])

    def test_string_argument(self):
        sys.argv = ["testcmd", "--host=localhost"]
        values, messages = cmdline_config.get(self.options)
        self.assertEqual(values.host, "localhost")

    def test_integer_argument(self):
        sys.argv = ["testcmd", "--port=12345"]
        values, messages = cmdline_config.get(self.options)
        self.assertEqual(values.port, 12345)

    def test_boolean_argument(self):
        sys.argv = ["testcmd", "--allow"]
        values, messages = cmdline_config.get(self.options)
        self.assertEqual(values.allow, True)

    def test_multiple_arguments(self):
        sys.argv = ["testcmd", "file1.txt", "file2.txt"]
        values, messages = cmdline_config.get(self.options)
        self.assertEqual(values.file, ["file1.txt", "file2.txt"])

    def test_all_arguments(self):
        sys.argv = [
            "testcmd",
            "--host=localhost",
            "--port=12345",
            "--allow",
            "file1.txt",
            "file2.txt",
        ]
        values, messages = cmdline_config.get(self.options)
        self.assertEqual(values.host, "localhost")
        self.assertEqual(values.port, 12345)
        self.assertEqual(values.allow, True)
        self.assertEqual(values.file, ["file1.txt", "file2.txt"])
