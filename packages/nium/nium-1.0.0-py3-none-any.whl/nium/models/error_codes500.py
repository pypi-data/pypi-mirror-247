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





class ErrorCodes500(str, Enum):
    """
    The detailed error code associated with HTTP status 500. * `fx_dependency_error`: Error happens when the service calls its dependencies. * `fx_uncategorized_error`: Service errors not categorized. 
    """

    """
    allowed enum values
    """
    FX_DEPENDENCY_ERROR = 'fx_dependency_error'
    FX_UNCATEGORIZED_ERROR = 'fx_uncategorized_error'

    @classmethod
    def from_str(cls, input_str: str) -> "ErrorCodes500":
        """Create an instance of ErrorCodes500 from a string"""
        return ErrorCodes500(input_str)


