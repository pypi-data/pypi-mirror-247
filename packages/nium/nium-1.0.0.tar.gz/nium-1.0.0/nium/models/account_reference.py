# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr

class AccountReference(BaseModel):
    """
    AccountReference
    """
    bban: Optional[StrictStr] = Field(None, description="This field contains the Basic Bank Account Number (BBAN) Identifier. This data elements is used for payment accounts which have no IBAN, for example, \"BARC12345612345678\"")
    currency: Optional[StrictStr] = Field(None, description="This field contains the debtor’s 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    iban: Optional[StrictStr] = Field(None, description="This field contains the International Bank Account Number (IBAN) for the debtor’s account, for example, \"FR7612345987650123456789014\".")
    masked_pan: Optional[StrictStr] = Field(None, alias="maskedPan", description="This field contains the masked Primary Account Number (PAN) of the debtor’s card. Masked data is represented by *.")
    msisdn: Optional[StrictStr] = Field(None, description="This field contains an alias to access a payment account via a registered mobile phone number.")
    pan: Optional[StrictStr] = Field(None, description="This field contains the Primary Account Number (PAN) of the debtor’s card, can be tokenized by the ASPSP due to PCI DSS requirements.")
    __properties = ["bban", "currency", "iban", "maskedPan", "msisdn", "pan"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountReference:
        """Create an instance of AccountReference from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccountReference:
        """Create an instance of AccountReference from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccountReference.parse_obj(obj)

        _obj = AccountReference.parse_obj({
            "bban": obj.get("bban"),
            "currency": obj.get("currency"),
            "iban": obj.get("iban"),
            "masked_pan": obj.get("maskedPan"),
            "msisdn": obj.get("msisdn"),
            "pan": obj.get("pan")
        })
        return _obj


