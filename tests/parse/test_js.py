import unittest

from tplink_wr.parse import js


TEST_SCRIPT = """
var first = "something";
var doubled = true;
var second = new Array(1, 2,
3);
var third = 5;
var doubled = false;
"""


class TestFindJSVar(unittest.TestCase):
    def test_exist_one(self):
        var = js.find_var("first", TEST_SCRIPT)
        self.assertEqual(var, '"something"')

    def test_exist_few(self):
        var = js.find_var("doubled", TEST_SCRIPT)
        self.assertEqual(var, "true")

    def test_not_exist(self):
        var = js.find_var("abc", TEST_SCRIPT)
        self.assertIsNone(var)

    def test_multiline(self):
        var = js.find_var("second", TEST_SCRIPT)
        self.assertEqual(var, "new Array(1, 2,\n3)")


class TestParseJSVar(unittest.TestCase):
    def test_primitive(self):
        self.assertEqual(
            js.parse_primitive("123"),
            123,
        )

    def test_primitive_arg(self):
        self.assertEqual(
            js.parse_primitive("123", strip_zeros=False),
            123,
        )

    def test_array(self):
        self.assertEqual(
            js.parse_array('new Array(1, 2, "str", 0, 0)'),
            [1, 2, "str"],
        )

    def test_array_arg(self):
        self.assertEqual(
            js.parse_array('new Array(1, 2, "str", 0, 0)', strip_zeros=False),
            [1, 2, "str", 0, 0],
        )

    def test_unknown(self):
        self.assertIsNone(
            js.parse_array("notavalue"),
        )


class TestParseJSPrimitive(unittest.TestCase):
    def test_int(self):
        self.assertEqual(
            js.parse_primitive("0"),
            0,
        )
        self.assertEqual(
            js.parse_primitive("123"),
            123,
        )
        self.assertEqual(
            js.parse_primitive("-1"),
            -1,
        )

    def test_bool(self):
        self.assertEqual(
            js.parse_primitive("true"),
            True,
        )
        self.assertEqual(
            js.parse_primitive("false"),
            False,
        )

    def test_str(self):
        self.assertEqual(
            js.parse_primitive('""'),
            "",
        )
        self.assertEqual(
            js.parse_primitive('"some string"'),
            "some string",
        )

    def test_list(self):
        self.assertEqual(
            js.parse_primitive('[]'),
            [],
        )
        self.assertEqual(
            js.parse_primitive('[1, 2, "str"]'),
            [1, 2, "str"],
        )

    def test_unknown(self):
        self.assertIsNone(
            js.parse_primitive("notavalue"),
        )
        self.assertIsNone(
            js.parse_primitive("5 + 6"),
        )


class TestParseJSArray(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            js.parse_array("new Array()"),
            [],
        )

    def test_filled(self):
        self.assertEqual(
            js.parse_array('new Array(1, 2, "str", 0, 0)'),
            [1, 2, "str"],
        )

    def test_filled_raw(self):
        self.assertEqual(
            js.parse_array('new Array(1, 2, "str", 0, 0)', strip_zeros=False),
            [1, 2, "str", 0, 0],
        )

    def test_wrong(self):
        self.assertIsNone(
            js.parse_array("17"),
        )


class TestGetJSVar(unittest.TestCase):
    def test_exist(self):
        self.assertEqual(
            js.get_var("third", TEST_SCRIPT),
            5,
        )

    def test_multiline(self):
        self.assertEqual(
            js.get_var("second", TEST_SCRIPT, strip_zeros=False),
            [1, 2, 3],
        )

    def test_not_exist(self):
        self.assertIsNone(
            js.get_var("abc", TEST_SCRIPT),
        )
