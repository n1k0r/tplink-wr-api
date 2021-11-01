import json
import re


def find_var(name: str, script: str):
    match = re.search(f"\s+{name}\s*=\s*([^\s]([\s\S]*?[^\s])??)\s*;", script)
    if not match:
        return None
    return match.group(1)


def parse_var(var: str, **kwargs):
    if (array := parse_array(var, **kwargs)) is not None:
        return array

    return parse_primitive(var, **kwargs)


def parse_primitive(value: str, **kwargs):
    try:
        result = json.loads(value)
    except json.decoder.JSONDecodeError:
        return None

    return result


def parse_array(value: str, strip_zeros=True, **kwargs):
    if not (match := re.match(f"new\s+Array\(([\s\S]*)\)", value)):
        return None

    content = match.group(1)
    value_wrapped = f"[{content}]"
    values = parse_primitive(value_wrapped)

    if strip_zeros and list(values[-2:]) == [0, 0]:
        values = values[:-2]

    return values


def get_var(name: str, script: str, **kwargs):
    var = find_var(name, script)
    if not var:
        return None

    value = parse_var(var, **kwargs)
    return value
