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





class ErrorCodes403(str, Enum):
    """
    The detailed error code associated with HTTP status 403. * `fx_client_no_access`: The client is authenticated but not authorized. 
    """

    """
    allowed enum values
    """
    FX_CLIENT_NO_ACCESS = 'fx_client_no_access'

    @classmethod
    def from_str(cls, input_str: str) -> "ErrorCodes403":
        """Create an instance of ErrorCodes403 from a string"""
        return ErrorCodes403(input_str)


