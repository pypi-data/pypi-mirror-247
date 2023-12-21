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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class RemitterAccountWhiteList(BaseModel):
    """
    RemitterAccountWhiteList
    """
    active: Optional[StrictBool] = Field(None, description="This field will return true if the remittance account is active else this will return false")
    remitter_account_number: Optional[StrictStr] = Field(None, alias="remitterAccountNumber", description="This field contains the remitter account number, for example, 9890098900")
    remitter_allowed_currency: Optional[StrictStr] = Field(None, alias="remitterAllowedCurrency", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the allowed remittance currencies.")
    __properties = ["active", "remitterAccountNumber", "remitterAllowedCurrency"]

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
    def from_json(cls, json_str: str) -> RemitterAccountWhiteList:
        """Create an instance of RemitterAccountWhiteList from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RemitterAccountWhiteList:
        """Create an instance of RemitterAccountWhiteList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RemitterAccountWhiteList.parse_obj(obj)

        _obj = RemitterAccountWhiteList.parse_obj({
            "active": obj.get("active"),
            "remitter_account_number": obj.get("remitterAccountNumber"),
            "remitter_allowed_currency": obj.get("remitterAllowedCurrency")
        })
        return _obj


