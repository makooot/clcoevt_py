import os
import typing
import unittest

from clcoevt.envvar_config import envvar_get
from clcoevt.types import ClcoevtCliOption


class TestEnvvarConfig(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.options: list[ClcoevtCliOption] = [
            {"key": "db_host", "envvar": "DB_HOST", "type": "string"},
            {"key": "db_port", "envvar": "DB_PORT", "type": "int"},
            {"key": "allow", "envvar": "ALLOW", "type": "bool"},
        ]
        os.environ["DB_HOST"] = ""
        os.environ["DB_PORT"] = "0"
        os.environ["ALLOW"] = "true"

    def test_invalid_envvars(self):
        options: list[ClcoevtCliOption] = [{"key": "a", "envvar": "A"}]
        _, warn_log = envvar_get(options)
        for warning in warn_log:
            if (
                str(warning)
                == "clcoevt-env: Invalid setting: {'key': 'a', 'envvar': 'A'}"
            ):
                break
        else:
            self.fail("Warning not found: clcoevt-env: Invalid setting:")

    def test_not_defined(self):
        del os.environ["DB_HOST"]
        values, warn_log = envvar_get(self.options)
        self.assertFalse("db_host" in values)
        for warning in warn_log:
            if str(warning) == "clcoevt-env: Environment variable not found: DB_HOST":
                break
        else:
            self.fail("Warning not found: clcoevt-env: Environment variable not found:")

    def test_null_string(self):
        os.environ["DB_HOST"] = ""
        values, _ = envvar_get(self.options)
        self.assertEqual(values["db_host"], "")

    def test_string_of_some_length(self):
        os.environ["DB_HOST"] = "localhost"
        values, _ = envvar_get(self.options)
        self.assertEqual(values["db_host"], "localhost")

    def test_null_int(self):
        os.environ["DB_PORT"] = ""
        values, warn_log = envvar_get(self.options)
        self.assertFalse("db_port" in values)
        self.assertEqual(str(warn_log[0]), "clcoevt-env: Invalid value: DB_PORT")

    def test_invalid_int(self):
        os.environ["DB_PORT"] = "abc"
        values, warn_log = envvar_get(self.options)
        self.assertFalse("db_port" in values)
        self.assertEqual(str(warn_log[0]), "clcoevt-env: Invalid value: DB_PORT")

    def test_positive_integer(self):
        os.environ["DB_PORT"] = "12345"
        values, warn_log = envvar_get(self.options)
        self.assertEqual(values["db_port"], 12345)

    def test_negative_integer(self):
        os.environ["DB_PORT"] = "-12345"
        values, _ = envvar_get(self.options)
        self.assertEqual(values["db_port"], -12345)

    def test_zero(self):
        os.environ["DB_PORT"] = "0"
        values, _ = envvar_get(self.options)
        self.assertEqual(values["db_port"], 0)

    def test_bool_true(self):
        os.environ["ALLOW"] = "true"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "t"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "yes"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "y"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "on"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "1"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "anystring"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "True"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "T"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "Yes"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "Y"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])
        os.environ["ALLOW"] = "On"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_bool_false(self):
        os.environ["ALLOW"] = "false"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "f"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "no"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "n"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "off"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "0"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = ""
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "False"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "F"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "No"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "N"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
        os.environ["ALLOW"] = "Off"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])

