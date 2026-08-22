import unittest
import os
import typing
import clcoevt.envvar_config as envvar_config
import clcoevt.types as types


class TestEnvvarConfig(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.options = [
            types.ClcoevtCliOption(key="db_host", envvar="DB_HOST", type="string"),
            types.ClcoevtCliOption(key="db_port", envvar="DB_PORT", type="int"),
            types.ClcoevtCliOption(key="allow", envvar="ALLOW", type="bool"),
        ]
        os.environ["DB_HOST"] = ""
        os.environ["DB_PORT"] = "0"
        os.environ["ALLOW"] = "true"

    def test_invalid_envvars(self):
        options = [types.ClcoevtCliOption(key="a", envvar="A")]
        values, messages = envvar_config.get(options)
        self.assertEqual(messages[0].msgid, "INVALID_SETTING")

    def test_not_defined(self):
        del os.environ["DB_HOST"]
        values, messages = envvar_config.get(self.options)
        self.assertFalse(hasattr(values, "dp_host"))
        self.assertEqual(messages[0].msgid, "NOT_FOUND")
        self.assertEqual(messages[0].text, "Not found: DB_HOST")

    def test_null_string(self):
        os.environ["DB_HOST"] = ""
        values, messages = envvar_config.get(self.options)
        self.assertEqual(values.db_host, "")

    def test_string_of_some_length(self):
        os.environ["DB_HOST"] = "localhost"
        values, messages = envvar_config.get(self.options)
        self.assertEqual(values.db_host, "localhost")

    def test_null_int(self):
        os.environ["DB_PORT"] = ""
        values, messages = envvar_config.get(self.options)
        self.assertFalse(hasattr(values, "dp_port"))
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: DB_PORT=")

    def test_invalid_int(self):
        os.environ["DB_PORT"] = "abc"
        values, messages = envvar_config.get(self.options)
        self.assertFalse(hasattr(values, "dp_port"))
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: DB_PORT=abc")

    def test_positive_integer(self):
        os.environ["DB_PORT"] = "12345"
        values, messages = envvar_config.get(self.options)
        self.assertEqual(values.db_port, 12345)

    def test_negative_integer(self):
        os.environ["DB_PORT"] = "-12345"
        values, messages = envvar_config.get(self.options)
        self.assertEqual(values.db_port, -12345)

    def test_zero(self):
        os.environ["DB_PORT"] = "0"
        values, messages = envvar_config.get(self.options)
        self.assertEqual(values.db_port, 0)

    def test_null_bool(self):
        os.environ["ALLOW"] = ""
        values, messages = envvar_config.get(self.options)
        self.assertFalse(hasattr(values, "allow"))
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: ALLOW=")

    def test_invalid_bool(self):
        os.environ["ALLOW"] = "1"
        values, messages = envvar_config.get(self.options)
        self.assertFalse(hasattr(values, "allow"))
        self.assertEqual(messages[0].msgid, "INVALID_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: ALLOW=1")

    def test_true(self):
        os.environ["ALLOW"] = "true"
        values, messages = envvar_config.get(self.options)
        self.assertTrue(values.allow)

    def test_false(self):
        os.environ["ALLOW"] = "false"
        values, messages = envvar_config.get(self.options)
        self.assertFalse(values.allow)
