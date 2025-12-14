import unittest
import sys
import clcoevt.cmdline_config as cmdline_config


class TestEnvvarConfig(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "command": {
                "name": "testcmd",
                "version": "1.2.3",
                "argument": {
                    "file": {"num": "0+"},
                },
            },
            "options": {
                "host": {"cmd": ["--host"], "type": "string"},
                "port": {"cmd": ["--port"], "type": "int"},
                "allow": {"cmd": ["--allow"], "type": "bool"},
            },
        }

    def test_invalid_setting_no_command_name(self):
        settings = {
            "command": {},
            "options": {},
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(settings["command"], settings["options"])

    def test_invalid_setting_no_command_version(self):
        settings = {
            "command": {"name": "testcmd"},
            "options": {},
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(settings["command"], settings["options"])

    def test_invalid_setting_unsuported_option_type(self):
        settings = {
            "command": {
                "name": "testcmd",
                "version": "1.2.3",
            },
            "options": {
                "opt1": {"cmd": ["--opt1"], "type": "unsuported_type"},
            },
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(settings["command"], settings["options"])

    def test_invalid_setting_invalid_argument_num(self):
        settings = {
            "command": {
                "name": "testcmd",
                "version": "1.2.3",
                "argument": {"arg1": {"num": "invalid_num"}},
            },
            "options": {},
        }
        with self.assertRaises(ValueError):
            cmdline_config.get(settings["command"], settings["options"])

    def test_no_arguments(self):
        sys.argv = ["testcmd"]
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
        self.assertFalse(hasattr(values, "host"))
        self.assertFalse(hasattr(values, "port"))
        self.assertFalse(hasattr(values, "allow"))
        self.assertEqual(values.file, [])

    def test_string_argument(self):
        sys.argv = ["testcmd", "--host=localhost"]
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
        self.assertEqual(values.host, "localhost")

    def test_integer_argument(self):
        sys.argv = ["testcmd", "--port=12345"]
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
        self.assertEqual(values.port, 12345)

    def test_boolean_argument(self):
        sys.argv = ["testcmd", "--allow"]
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
        self.assertEqual(values.allow, True)

    def test_multiple_arguments(self):
        sys.argv = ["testcmd", "file1.txt", "file2.txt"]
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
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
        values, messages = cmdline_config.get(
            self.settings["command"], self.settings["options"]
        )
        self.assertEqual(values.host, "localhost")
        self.assertEqual(values.port, 12345)
        self.assertEqual(values.allow, True)
        self.assertEqual(values.file, ["file1.txt", "file2.txt"])
