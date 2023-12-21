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





class ErrorCodes400(str, Enum):
    """
    The detailed error code associated with HTTP status 400.  * `fx_constraint_violated_input`: The input violates the model constraints. * `fx_invalid_format_input`: The input format is invalid. * `fx_invalid_currency_code`: The input currency code is invalid. * `fx_missing_input`: The required fields are missing. * `fx_date_range_invalid`: The date range should be within 90 days. 
    """

    """
    allowed enum values
    """
    FX_CONSTRAINT_VIOLATED_INPUT = 'fx_constraint_violated_input'
    FX_INVALID_FORMAT_INPUT = 'fx_invalid_format_input'
    FX_INVALID_CURRENCY_CODE = 'fx_invalid_currency_code'
    FX_MISSING_INPUT = 'fx_missing_input'
    FX_DATE_RANGE_INVALID = 'fx_date_range_invalid'

    @classmethod
    def from_str(cls, input_str: str) -> "ErrorCodes400":
        """Create an instance of ErrorCodes400 from a string"""
        return ErrorCodes400(input_str)


