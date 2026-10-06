import typing
import unittest

from clcoevt.tomlfile_config import tomlfile_get
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
        _, warn_log = tomlfile_get(
            "file_not_found.toml", "", self.clcoevt_config["options"]
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: File not found: file_not_found.toml":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: File not found:")

    def test_empty_file(self):
        _, warn_log = tomlfile_get(
            "test-data/empty.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(len(warn_log), 0)

    def test_invalid_file(self):
        _, warn_log = tomlfile_get(
            "test-data/invalid.toml", "", self.clcoevt_config["options"]
        )
        for warning in warn_log:
            if (
                str(warning)
                == "clcoevt-toml: Invalid TOML file: test-data/invalid.toml"
            ):
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid TOML file:")

    def test_empty_string(self):
        values, _ = tomlfile_get(
            "test-data/empty_string.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(values["host"], "")

    def test_zero_int(self):
        values, _ = tomlfile_get(
            "test-data/zero_int.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(values["port"], 0)

    def test_negative_int(self):
        values, _ = tomlfile_get(
            "test-data/negative_int.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(values["port"], -12345)

    def test_positive_int(self):
        values, _ = tomlfile_get(
            "test-data/positive_int.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(values["port"], 12345)

    def test_bool_true(self):
        values, _ = tomlfile_get(
            "test-data/true.toml", "", self.clcoevt_config["options"]
        )
        self.assertTrue(values["allow"])

    def test_bool_false(self):
        values, _ = tomlfile_get(
            "test-data/false.toml", "", self.clcoevt_config["options"]
        )
        self.assertFalse(values["allow"])

    def test_valid_file(self):
        values, _ = tomlfile_get(
            "test-data/valid.toml", "", self.clcoevt_config["options"]
        )
        self.assertEqual(values["host"], "localhost")
        self.assertEqual(values["port"], 12345)
        self.assertTrue(values["allow"])

    def test_unmatch_typeInt_valueString(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_int-value_string.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: PORT":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_unmatch_typeString_valueInt(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_string-value_int.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: HOST":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_unmatch_typeBool_valueInt(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_bool-value_int.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: ALLOW":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_unmatch_typeInt_valueBool(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_int-value_bool.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: PORT":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_unmatch_typeString_valueBool(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_string-value_bool.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: HOST":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_unmatch_typeBool_valueString(self):
        _, warn_log = tomlfile_get(
            "test-data/unmatch-type_bool-value_string.toml",
            "",
            self.clcoevt_config["options"],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Invalid value: ALLOW":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Invalid value:")

    def test_table_not_found(self):
        _, warn_log = tomlfile_get(
            "test-data/valid.toml", "nonexistent_table", self.clcoevt_config["options"]
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Table not found: nonexistent_table":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Table not found:")

    def test_table_found(self):
        values, _ = tomlfile_get(
            "test-data/valid.toml", "my_table", self.clcoevt_config["options"]
        )
        self.assertEqual(values["host"], "tablehost")
        self.assertEqual(values["port"], 12399)
        self.assertTrue(values["allow"])

    def test_nested_table_found(self):
        values, _ = tomlfile_get(
            "test-data/valid.toml",
            "table.nestedtable",
            self.clcoevt_config["options"],
        )
        self.assertEqual(values["host"], "nestedtable")
        self.assertEqual(values["port"], 12388)
        self.assertTrue(values["allow"])

    def test_dotted_key(self):
        values, _ = tomlfile_get(
            "test-data/valid.toml",
            "dottedkey",
            [
                {"key": "host", "toml": "server.HOST", "type": "string"},
                {"key": "port", "toml": "server.PORT", "type": "int"},
                {"key": "allow", "toml": "server.ALLOW", "type": "bool"},
            ],
        )
        self.assertEqual(values["host"], "dottedkey")
        self.assertEqual(values["port"], 12377)
        self.assertTrue(values["allow"])

    def test_table_not_found_with_dotted_key(self):
        _, warn_log = tomlfile_get(
            "test-data/valid.toml",
            "nonexistent_table",
            [],
        )
        for warning in warn_log:
            if str(warning) == "clcoevt-toml: Table not found: nonexistent_table":
                break
        else:
            self.fail("Warning not found: clcoevt-toml: Table not found:")
