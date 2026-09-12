import unittest
import typing
from clcoevt.cmdline_config import cmdline_get
from clcoevt.types import (
    ClcoevtCommandDetail,
    ClcoevtShowHelpException,
    ClcoevtShowVersionException,
    ClcoevtValueError,
)


class TestEnvvarConfig(unittest.TestCase):
    @typing.override
    def setUp(self):
        pass

    def test_empty(self):
        args = []
        command_detail: ClcoevtCommandDetail = {}
        _, unnamed = cmdline_get(command_detail, args)
        self.assertEqual(unnamed, [])

    def test_args_1(self):
        args = ["v1"]
        command_detail: ClcoevtCommandDetail = {}
        _, unnamed = cmdline_get(command_detail, args)
        self.assertEqual(unnamed, ["v1"])

    def test_args_2(self):
        args = ["v1", "v2"]
        command_detail: ClcoevtCommandDetail = {}
        _, unnamed = cmdline_get(command_detail, args)
        self.assertEqual(unnamed, ["v1", "v2"])

    def test_args_3(self):
        args = ["v1", "v2", "v3"]
        command_detail: ClcoevtCommandDetail = {}
        _, unnamed = cmdline_get(command_detail, args)
        self.assertEqual(unnamed, ["v1", "v2", "v3"])

    def test_short_bool(self):
        args = ["-b"]
        command_detail: ClcoevtCommandDetail = {
            "options": [{"key": "b", "type": "bool", "cmd": ["-b"]}]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["b"])

    def test_short_string_connected(self):
        args = ["-s=foo"]
        command_detail: ClcoevtCommandDetail = {
            "options": [{"key": "s", "type": "string", "cmd": ["-s"]}]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["s"], "foo")

    def test_short_string_seperated(self):
        args = ["-s", "foo"]
        command_detail: ClcoevtCommandDetail = {
            "options": [{"key": "s", "type": "string", "cmd": ["-s"]}]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["s"], "foo")

    def test_short_int_connected(self):
        args = ["-n=123"]
        command_detail: ClcoevtCommandDetail = {
            "options": [{"key": "n", "type": "int", "cmd": ["-n"]}]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["n"], 123)

    def test_short_int_seperated(self):
        args = ["-n", "123"]
        command_detail: ClcoevtCommandDetail = {
            "options": [{"key": "n", "type": "int", "cmd": ["-n"]}]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["n"], 123)

    def test_short_chain_bbb(self):
        args = ["-abc"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "a", "type": "bool", "cmd": ["-a"]},
                {"key": "b", "type": "bool", "cmd": ["-b"]},
                {"key": "c", "type": "bool", "cmd": ["-c"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["a"])
        self.assertTrue(opts["b"])
        self.assertTrue(opts["c"])

    def test_short_chain_bbs_empty(self):
        args = ["-abs="]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "a", "type": "bool", "cmd": ["-a"]},
                {"key": "b", "type": "bool", "cmd": ["-b"]},
                {"key": "c", "type": "bool", "cmd": ["-c"]},
                {"key": "s", "type": "string", "cmd": ["-s"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["a"])
        self.assertTrue(opts["b"])
        self.assertEqual(opts["s"], "")

    def test_short_chain_bbs_any(self):
        args = ["-abs=foo"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "a", "type": "bool", "cmd": ["-a"]},
                {"key": "b", "type": "bool", "cmd": ["-b"]},
                {"key": "c", "type": "bool", "cmd": ["-c"]},
                {"key": "s", "type": "string", "cmd": ["-s"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["a"])
        self.assertTrue(opts["b"])
        self.assertEqual(opts["s"], "foo")

    def test_short_chain_bbi(self):
        args = ["-abn=1234"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "a", "type": "bool", "cmd": ["-a"]},
                {"key": "b", "type": "bool", "cmd": ["-b"]},
                {"key": "n", "type": "int", "cmd": ["-n"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["a"])
        self.assertTrue(opts["b"])
        self.assertEqual(opts["n"], 1234)

    def test_long_bool(self):
        args = ["--allow"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "allow", "type": "bool", "cmd": ["--allow"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertTrue(opts["allow"])

    def test_long_string_connected_empty(self):
        args = ["--prefix="]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "prefix", "type": "string", "cmd": ["--prefix"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["prefix"], "")

    def test_long_string_connected_any(self):
        args = ["--prefix=I:"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "prefix", "type": "string", "cmd": ["--prefix"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["prefix"], "I:")

    def test_long_string_seperated(self):
        args = ["--prefix", "I:"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "prefix", "type": "string", "cmd": ["--prefix"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["prefix"], "I:")

    def test_long_int_connected(self):
        args = ["--port=8080"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["port"], 8080)

    def test_long_int_seperated(self):
        args = ["--port", "8080"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["port"], 8080)

    def test_both_def_short(self):
        args = ["-p=8080"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["-p", "--port"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["port"], 8080)

    def test_both_def_long(self):
        args = ["--port=8080"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["-p", "--port"]},
            ]
        }
        opts, _ = cmdline_get(command_detail, args)
        self.assertEqual(opts["port"], 8080)

    def test_mix(self):
        args = ["-ap", "8080", "--prefix=BEEF", "jkl", "mno"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "allow", "type": "bool", "cmd": ["-a", "--allow"]},
                {"key": "port", "type": "int", "cmd": ["-p", "--port"]},
                {"key": "prefix", "type": "string", "cmd": ["-x", "--prefix"]},
            ]
        }
        opts, unnamed = cmdline_get(command_detail, args)
        self.assertTrue(opts["allow"])
        self.assertEqual(opts["prefix"], "BEEF")
        self.assertEqual(opts["port"], 8080)
        self.assertEqual(unnamed, ["jkl", "mno"])

    def test_double_hyphen(self):
        args = ["-ap", "8080", "--", "--prefix=BEEF", "jkl", "mno"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "allow", "type": "bool", "cmd": ["-a", "--allow"]},
                {"key": "prefix", "type": "string", "cmd": ["-x", "--prefix"]},
                {"key": "port", "type": "int", "cmd": ["-p", "--port"]},
            ]
        }
        opts, unnamed = cmdline_get(command_detail, args)
        self.assertTrue(opts["allow"])
        self.assertEqual(opts["port"], 8080)
        self.assertEqual(unnamed, ["--prefix=BEEF", "jkl", "mno"])

    def test_short_invalid_name(self):
        args = ["-#"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_short_undefined_name(self):
        args = ["-q"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_long_invalid_name(self):
        args = ["--###-###"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_invlid_int_1(self):
        args = ["--port", "0A"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_invlid_int_2(self):
        args = ["--port=0A"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_invlid_int_3(self):
        args = ["-p", "0A"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_invlid_int_4(self):
        args = ["-p=0A"]
        command_detail: ClcoevtCommandDetail = {
            "options": [
                {"key": "port", "type": "int", "cmd": ["--port"]},
            ]
        }
        with self.assertRaises(ClcoevtValueError):
            cmdline_get(command_detail, args)

    def test_invalid_name_1(self):
        args = ["--verbose"]
        with self.assertRaises(ClcoevtValueError):
            cmdline_get({}, args)

    def test_invalid_name_2(self):
        args = ["-v"]
        with self.assertRaises(ClcoevtValueError):
            cmdline_get({}, args)

    def test_short_showhelp_exception(self):
        args = ["-h"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtShowHelpException):
            cmdline_get(command_detail, args)

    def test_long_showhelp_exception(self):
        args = ["--help"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtShowHelpException):
            cmdline_get(command_detail, args)

    def test_long_showversion_exception(self):
        args = ["--version"]
        command_detail: ClcoevtCommandDetail = {}
        with self.assertRaises(ClcoevtShowVersionException):
            cmdline_get(command_detail, args)
