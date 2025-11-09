import unittest
import clcoevt_py.tomlfile_config as tomlfile_config


class TestTomlfileConfig(unittest.TestCase):
    def setUp(self):
        self.clcoevt_config = {
            "option": {
                "host": {"toml": "HOST", "type": "string"},
                "port": {"toml": "PORT", "type": "int"},
                "allow": {"toml": "ALLOW", "type": "bool"},
            },
        }

    def test_file_not_found(self):
        values, messages = tomlfile_config.get(
            "file_not_found.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(messages[0].msgid, "FILE_NOT_FOUND")
        self.assertEqual(messages[0].text, "File not found: file_not_found.toml")

    def test_empty_file(self):
        values, messages = tomlfile_config.get(
            "test-data/empty.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)

    def test_invalid_file(self):
        values, messages = tomlfile_config.get(
            "test-data/invalid.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_FILE")
        self.assertEqual(messages[0].text, "Invalid TOML file: test-data/invalid.toml")

    def test_empty_string(self):
        values, messages = tomlfile_config.get(
            "test-data/empty_string.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertEqual(values.host, "")

    def test_zero_int(self):
        values, messages = tomlfile_config.get(
            "test-data/zero_int.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertEqual(values.port, 0)

    def test_negative_int(self):
        values, messages = tomlfile_config.get(
            "test-data/negative_int.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertEqual(values.port, -12345)

    def test_positive_int(self):
        values, messages = tomlfile_config.get(
            "test-data/positive_int.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertEqual(values.port, 12345)

    def test_bool_true(self):
        values, messages = tomlfile_config.get(
            "test-data/true.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertTrue(values.allow)

    def test_bool_false(self):
        values, messages = tomlfile_config.get(
            "test-data/false.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertFalse(values.allow)

    def test_valid_file(self):
        values, messages = tomlfile_config.get(
            "test-data/valid.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(len(messages), 0)
        self.assertEqual(values.host, "localhost")
        self.assertEqual(values.port, 12345)
        self.assertTrue(values.allow)

    def test_unmatch_typeInt_valueString(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_int-value_string.toml",
            self.clcoevt_config["option"],
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, 'Invalid value: PORT="x"')

    def test_unmatch_typeString_valueInt(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_string-value_int.toml",
            self.clcoevt_config["option"],
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: HOST=0")

    def test_unmatch_typeBool_valueInt(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_bool-value_int.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: ALLOW=0")

    def test_unmatch_typeInt_valueBool(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_int-value_bool.toml", self.clcoevt_config["option"]
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: PORT=true")

    def test_unmatch_typeString_valueBool(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_string-value_bool.toml",
            self.clcoevt_config["option"],
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, "Invalid value: HOST=true")

    def test_unmatch_typeBool_valueString(self):
        values, messages = tomlfile_config.get(
            "test-data/unmatch-type_bool-value_string.toml",
            self.clcoevt_config["option"],
        )
        self.assertEqual(messages[0].msgid, "INVALID_TOML_VALUE")
        self.assertEqual(messages[0].text, 'Invalid value: ALLOW="x"')
