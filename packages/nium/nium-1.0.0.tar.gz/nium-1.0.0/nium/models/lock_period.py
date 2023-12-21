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





class LockPeriod(str, Enum):
    """
    The duration for which the quote remains valid after creation.
    """

    """
    allowed enum values
    """
    ENUM_5_MINS = '5_mins'
    ENUM_15_MINS = '15_mins'
    ENUM_1_HOUR = '1_hour'
    ENUM_4_HOURS = '4_hours'
    ENUM_8_HOURS = '8_hours'
    ENUM_24_HOURS = '24_hours'

    @classmethod
    def from_str(cls, input_str: str) -> "LockPeriod":
        """Create an instance of LockPeriod from a string"""
        return LockPeriod(input_str)


