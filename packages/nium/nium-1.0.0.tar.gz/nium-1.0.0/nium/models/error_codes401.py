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





class ErrorCodes401(str, Enum):
    """
    The detailed error code associated with HTTP status 401. * `fx_client_unauthenticated`: The client request lacks valid authentication credentials. 
    """

    """
    allowed enum values
    """
    FX_CLIENT_UNAUTHENTICATED = 'fx_client_unauthenticated'

    @classmethod
    def from_str(cls, input_str: str) -> "ErrorCodes401":
        """Create an instance of ErrorCodes401 from a string"""
        return ErrorCodes401(input_str)


