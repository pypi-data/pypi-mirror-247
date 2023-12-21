from typing import Any, List

from douban_crack.crack_data.crack_data import crack_data


def crack_html(html: str, **kwargs) -> List[Any]:
    """
    list of parsed window.__DATA__
    """
    lines = html.splitlines()
    result = []
    for line in lines:
        if line.strip().startswith("window.__DATA__"):
            result.append(crack_data(line.split('"')[1], **kwargs))
    return result
