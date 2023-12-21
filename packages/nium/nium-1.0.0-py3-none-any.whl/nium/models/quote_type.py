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





class QuoteType(str, Enum):
    """
    The type of the quote.   * `balance_transfer`: Quote for transferring the balance from one currency to another within the same customer wallet.   * `payout`: Quote for transferring money to a registered beneficiary's wallet in another currency. 
    """

    """
    allowed enum values
    """
    BALANCE_TRANSFER = 'balance_transfer'
    PAYOUT = 'payout'

    @classmethod
    def from_str(cls, input_str: str) -> "QuoteType":
        """Create an instance of QuoteType from a string"""
        return QuoteType(input_str)


