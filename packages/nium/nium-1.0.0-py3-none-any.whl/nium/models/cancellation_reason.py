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





class CancellationReason(str, Enum):
    """
    Reason for a conversion cancellation.    * `user_cancel`: User initiated cancellation.   * `insufficient_fund`: Cancellation due to insufficient balance in the wallet at the time of conversion execution. 
    """

    """
    allowed enum values
    """
    USER_CANCEL = 'user_cancel'
    INSUFFICIENT_FUND = 'insufficient_fund'

    @classmethod
    def from_str(cls, input_str: str) -> "CancellationReason":
        """Create an instance of CancellationReason from a string"""
        return CancellationReason(input_str)


