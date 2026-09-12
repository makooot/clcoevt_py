import unittest
import typing
import clcoevt.tomlfile_config as tomlfile_config
from clcoevt.types import ClcoevtCommandDetail


class TestTomlfileConfig(unittest.TestCase):
    @typing.override
    def setUp(self):
        self.clcoevt_config: ClcoevtCommandDetail = {
            "options": [
                {"key": "host", "toml": "HOST", "type": "string"},
                {"key": "port", "toml": "PORT", "type": "int"},
                {"key": "allow", "toml": "ALLOW", "type": "bool"},
            ]
        }

    def test_file_not_found(self):
        _, warn_log = tomlfile_config.get(
            "file_not_found.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(str(warn_log[0]), "File not found: file_not_found.toml")

    def test_empty_file(self):
        _, warn_log = tomlfile_config.get(
            "test-data/empty.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)

    def test_invalid_file(self):
        _, warn_log = tomlfile_config.get(
            "test-data/invalid.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(str(warn_log[0]), "Invalid TOML file: test-data/invalid.toml")

    def test_empty_string(self):
        values, warn_log = tomlfile_config.get(
            "test-data/empty_string.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertEqual(values["host"], "")

    def test_zero_int(self):
        values, warn_log = tomlfile_config.get(
            "test-data/zero_int.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertEqual(values["port"], 0)

    def test_negative_int(self):
        values, warn_log = tomlfile_config.get(
            "test-data/negative_int.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertEqual(values["port"], -12345)

    def test_positive_int(self):
        values, warn_log = tomlfile_config.get(
            "test-data/positive_int.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertEqual(values["port"], 12345)

    def test_bool_true(self):
        values, warn_log = tomlfile_config.get(
            "test-data/true.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertTrue(values["allow"])

    def test_bool_false(self):
        values, warn_log = tomlfile_config.get(
            "test-data/false.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertFalse(values["allow"])

    def test_valid_file(self):
        values, warn_log = tomlfile_config.get(
            "test-data/valid.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)
        self.assertEqual(values["host"], "localhost")
        self.assertEqual(values["port"], 12345)
        self.assertTrue(values["allow"])

    def test_unmatch_typeInt_valueString(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_int-value_string.toml",
            self.clcoevt_config["options"],
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for PORT: x")

    def test_unmatch_typeString_valueInt(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_string-value_int.toml",
            self.clcoevt_config["options"],
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for HOST: 0")

    def test_unmatch_typeBool_valueInt(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_bool-value_int.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for ALLOW: 0")

    def test_unmatch_typeInt_valueBool(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_int-value_bool.toml", self.clcoevt_config["options"]
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for PORT: True")

    def test_unmatch_typeString_valueBool(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_string-value_bool.toml",
            self.clcoevt_config["options"],
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for HOST: True")

    def test_unmatch_typeBool_valueString(self):
        values, warn_log = tomlfile_config.get(
            "test-data/unmatch-type_bool-value_string.toml",
            self.clcoevt_config["options"],
        )
        self.assertEqual(str(warn_log[0]), "Invalid value for ALLOW: x")
