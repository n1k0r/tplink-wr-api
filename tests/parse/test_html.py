import unittest

from tplink_wr.parse import html


class TestScriptFinder(unittest.TestCase):
    def test_exist(self):
        finder = html.ScriptFinder()
        finder.feed("<script>var abc = true;</script>")
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["var abc = true;"])

    def test_exist_uppercase(self):
        finder = html.ScriptFinder()
        finder.feed("<SCRIPT>var abc = true;</SCRIPT>")
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["var abc = true;"])

    def test_exist_multiline(self):
        finder = html.ScriptFinder()
        finder.feed("<script>\nvar abc = true;\nvar def = false;\n</script>")
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["\nvar abc = true;\nvar def = false;\n"])

    def test_exist_attrs(self):
        finder = html.ScriptFinder()
        finder.feed('<script language="javascript" type="text/javascript">var abc = true;</script>')
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["var abc = true;"])

    def test_exist_empty(self):
        finder = html.ScriptFinder()
        finder.feed("<script>\n</script>")
        scripts = finder.get_scripts()
        self.assertEqual(scripts, [])

    def test_exist_src(self):
        finder = html.ScriptFinder()
        finder.feed('<script language="javascript" src="../dynaform/common.js" type="text/javascript"></script>')
        scripts = finder.get_scripts()
        self.assertEqual(scripts, [])

    def test_exist_multiple(self):
        finder = html.ScriptFinder()
        finder.feed("""
        <script>var abc = true;</script>
        <script>var def = false;</script>
        """)
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["var abc = true;", "var def = false;"])

    def test_exist_other_tags(self):
        finder = html.ScriptFinder()
        finder.feed(""",
        <title>Some scripts here</title>
        <script>var abc = true;</script>
        <meta charset="utf-8">
        <script>var def = false;</script>
        <script language="javascript" src="../dynaform/common.js" type="text/javascript"></script>
        """)
        scripts = finder.get_scripts()
        self.assertEqual(scripts, ["var abc = true;", "var def = false;"])

    def test_exist_not_closed(self):
        finder = html.ScriptFinder()
        finder.feed('<script>var abc = "true";')
        scripts = finder.get_scripts()
        self.assertEqual(scripts, [])

    def test_not_exist(self):
        finder = html.ScriptFinder()
        finder.feed("""
        <title>No scripts here</title>
        <meta charset="utf-8">
        """)
        scripts = finder.get_scripts()
        self.assertEqual(scripts, [])

    def test_clear(self):
        finder = html.ScriptFinder()
        finder.feed("""
        <script>var abc = true;</script>
        <script>var def = false;</script>
        """)
        finder.close()
        finder.feed("""
        <title>No scripts here</title>
        <meta charset="utf-8">
        """)
        scripts = finder.get_scripts()
        self.assertEqual(len(scripts), 0)
