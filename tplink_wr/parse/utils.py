from . import html, js


def extract_vars(document: str, vars: list[str]):
    js_vars = {
        var: None
        for var in vars
    }

    scripts = html.find_scripts(document)
    for script in scripts:
        for var in js_vars:
            if js_vars[var] is None:
                js_vars[var] = js.get_var(var, script)

    return js_vars
