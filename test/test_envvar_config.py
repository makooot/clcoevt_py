import unittest
import os
import typing
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
        self.assertEqual(
            str(warn_log[0]), "Invalid setting: {'key': 'a', 'envvar': 'A'}"
        )

    def test_not_defined(self):
        del os.environ["DB_HOST"]
        values, warn_log = envvar_get(self.options)
        self.assertFalse("db_host" in values)
        self.assertEqual(str(warn_log[0]), "Environment variable not found: DB_HOST")

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
        self.assertEqual(str(warn_log[0]), "Invalid value for DB_PORT: ")

    def test_invalid_int(self):
        os.environ["DB_PORT"] = "abc"
        values, warn_log = envvar_get(self.options)
        self.assertFalse("db_port" in values)
        self.assertEqual(str(warn_log[0]), "Invalid value for DB_PORT: abc")

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

    def test_null_bool(self):
        os.environ["ALLOW"] = ""
        values, warn_log = envvar_get(self.options)
        self.assertFalse(values["allow"])

    def test_invalid_bool(self):
        os.environ["ALLOW"] = "1"
        values, warn_log = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_true(self):
        os.environ["ALLOW"] = "true"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_bool_t_is_true(self):
        os.environ["ALLOW"] = "t"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_bool_yes_is_true(self):
        os.environ["ALLOW"] = "yes"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_bool_y_is_true(self):
        os.environ["ALLOW"] = "y"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_bool_on_is_true(self):
        os.environ["ALLOW"] = "on"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_any_string_is_true(self):
        os.environ["ALLOW"] = "anystring"
        values, _ = envvar_get(self.options)
        self.assertTrue(values["allow"])

    def test_false(self):
        os.environ["ALLOW"] = "false"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])

    def test_bool_f_is_false(self):
        os.environ["ALLOW"] = "f"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])

    def test_bool_no_is_false(self):
        os.environ["ALLOW"] = "no"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])

    def test_bool_n_is_false(self):
        os.environ["ALLOW"] = "n"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])

    def test_bool_off_is_false(self):
        os.environ["ALLOW"] = "off"
        values, _ = envvar_get(self.options)
        self.assertFalse(values["allow"])
