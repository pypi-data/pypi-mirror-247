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





class ConversionStatus(str, Enum):
    """
    The status of the conversion.
    """

    """
    allowed enum values
    """
    CREATED = 'created'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    PENDING_CANCELLATION = 'pending_cancellation'

    @classmethod
    def from_str(cls, input_str: str) -> "ConversionStatus":
        """Create an instance of ConversionStatus from a string"""
        return ConversionStatus(input_str)


