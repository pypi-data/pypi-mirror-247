import re
from typing import Any, List

from douban_crack.crack_data.crack_data import crack_data_v0_0_2


def crack_html(html: str) -> List[Any]:
    """
    list of parsed window.__DATA__
    """
    data: str = re.search('window.__DATA__ = "([^"]+)"', html).group(1)  # 加密的数据
    return crack_data_v0_0_2(data)
