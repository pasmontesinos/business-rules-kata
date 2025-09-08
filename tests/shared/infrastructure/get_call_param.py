from typing import Any
from unittest.mock import Mock


def get_call_param(mock: Mock) -> Any:
    return mock.call_args[0][0]
