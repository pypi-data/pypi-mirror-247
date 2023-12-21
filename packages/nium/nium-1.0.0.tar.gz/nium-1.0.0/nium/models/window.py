# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class Window(str, Enum):
    """
    Specifies the field by which the results should be grouped.
    """

    """
    allowed enum values
    """
    ENUM_1_DAY = '1_day'
    ENUM_1_HOUR = '1_hour'

    @classmethod
    def from_str(cls, input_str: str) -> "Window":
        """Create an instance of Window from a string"""
        return Window(input_str)


