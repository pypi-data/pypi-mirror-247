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

class BankAccountDetails(BaseModel):
    """
    BankAccountDetails
    """
    account_name: Optional[StrictStr] = Field(None, alias="accountName")
    account_number: Optional[StrictStr] = Field(None, alias="accountNumber")
    bank_name: Optional[StrictStr] = Field(None, alias="bankName")
    currency: Optional[StrictStr] = None
    routing_type: Optional[StrictStr] = Field(None, alias="routingType")
    routing_value: Optional[StrictStr] = Field(None, alias="routingValue")
    __properties = ["accountName", "accountNumber", "bankName", "currency", "routingType", "routingValue"]

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
    def from_json(cls, json_str: str) -> BankAccountDetails:
        """Create an instance of BankAccountDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BankAccountDetails:
        """Create an instance of BankAccountDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BankAccountDetails.parse_obj(obj)

        _obj = BankAccountDetails.parse_obj({
            "account_name": obj.get("accountName"),
            "account_number": obj.get("accountNumber"),
            "bank_name": obj.get("bankName"),
            "currency": obj.get("currency"),
            "routing_type": obj.get("routingType"),
            "routing_value": obj.get("routingValue")
        })
        return _obj


