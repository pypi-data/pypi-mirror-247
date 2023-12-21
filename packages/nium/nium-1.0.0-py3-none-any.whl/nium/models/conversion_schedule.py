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





class ConversionSchedule(str, Enum):
    """
    The time period after which the conversion should be settled.
    """

    """
    allowed enum values
    """
    IMMEDIATE = 'immediate'
    END_OF_DAY = 'end_of_day'
    NEXT_DAY = 'next_day'
    ENUM_2_DAYS = '2_days'

    @classmethod
    def from_str(cls, input_str: str) -> "ConversionSchedule":
        """Create an instance of ConversionSchedule from a string"""
        return ConversionSchedule(input_str)


