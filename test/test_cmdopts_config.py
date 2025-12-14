import unittest
import os
import clcoevt.cmdopts_config as cmdopts_config


class TestCmdsOptsConfig(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "cmdopts": {
                "name": "TESTCMD_OPTS",
            },
            "option": {
                "host": {
                    "cmd": ["--host"],
                    "type": "string",
                },
                "port": {
                    "cmd": ["--port"],
                    "type": "int",
                },
                "allow": {
                    "cmd": ["--allow"],
                    "type": "bool",
                },
            },
        }

        self.cmd_opts = "TESTCMD_OPTS"
        os.environ[self.cmd_opts] = ""

    def test_no_cmd_opts(self):
        del os.environ[self.cmd_opts]
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(messages[0].msgid, "NOT_FOUND")
        self.assertEqual(
            messages[0].text, "Not found: Environment variable " + self.cmd_opts
        )

    def test_null(self):
        os.environ[self.cmd_opts] = ""
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 0)

    def test_invalid_opt(self):
        os.environ[self.cmd_opts] = "invalid"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")

    def test_string_1(self):
        os.environ[self.cmd_opts] = "--host=localhost"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertEqual(values.host, "localhost")
        self.assertEqual(len(messages), 0)

    def test_string_2(self):
        os.environ[self.cmd_opts] = "--host localhost"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertEqual(values.host, "localhost")
        self.assertEqual(len(messages), 0)

    def test_null_string(self):
        os.environ[self.cmd_opts] = "--host="
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertEqual(values.host, "")
        self.assertEqual(len(messages), 0)

    def test_int_1(self):
        os.environ[self.cmd_opts] = "--port=12345"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertEqual(values.port, 12345)
        self.assertEqual(len(messages), 0)

    def test_int_2(self):
        os.environ[self.cmd_opts] = "--port 12345"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertEqual(values.port, 12345)
        self.assertEqual(len(messages), 0)

    def test_bool(self):
        os.environ[self.cmd_opts] = "--allow"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 1)
        self.assertTrue(values.allow)
        self.assertEqual(len(messages), 0)

    def test_no_value_string(self):
        os.environ[self.cmd_opts] = "--host"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")

    def test_invalid_type_int(self):
        os.environ[self.cmd_opts] = "--port=x"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")

    def test_no_value_int(self):
        os.environ[self.cmd_opts] = "--port"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")

    def test_unnecessary_value_bool(self):
        os.environ[self.cmd_opts] = "--allow=0"
        values, messages = cmdopts_config.get(
            self.settings["cmdopts"]["name"], self.settings["option"]
        )
        self.assertEqual(len(vars(values)), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")
