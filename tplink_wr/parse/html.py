from html.parser import HTMLParser


class ScriptFinder(HTMLParser):
    def __init__(self):
        super().__init__()

        self.scripts = []
        self.script_in_progress = False

    def get_scripts(self):
        return self.scripts

    def close(self):
        super().close()

        self.scripts.clear()
        self.script_in_progress = False

    def handle_starttag(self, tag, attrs):
        if tag != "script":
            return

        self.script_in_progress = True
        self.current_script = ""

    def handle_endtag(self, tag):
        if tag != "script":
            return

        self.script_in_progress = False
        if self.current_script.strip():
            self.scripts.append(self.current_script)
        self.current_script = ""

    def handle_data(self, data):
        if not self.script_in_progress:
            return

        self.current_script += data


def find_scripts(data):
    finder = ScriptFinder()
    finder.feed(data)
    scripts = finder.get_scripts()
    return scripts
