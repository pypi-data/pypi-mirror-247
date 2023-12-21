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
from pydantic import BaseModel, Field
from nium.models.bank_account_details import BankAccountDetails
from nium.models.registered_address import RegisteredAddress

class AutoSweepBankDetails(BaseModel):
    """
    AutoSweepBankDetails
    """
    bank_account_details: Optional[BankAccountDetails] = Field(None, alias="bankAccountDetails")
    client_registered_address: Optional[RegisteredAddress] = Field(None, alias="clientRegisteredAddress")
    __properties = ["bankAccountDetails", "clientRegisteredAddress"]

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
    def from_json(cls, json_str: str) -> AutoSweepBankDetails:
        """Create an instance of AutoSweepBankDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of bank_account_details
        if self.bank_account_details:
            _dict['bankAccountDetails'] = self.bank_account_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of client_registered_address
        if self.client_registered_address:
            _dict['clientRegisteredAddress'] = self.client_registered_address.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AutoSweepBankDetails:
        """Create an instance of AutoSweepBankDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AutoSweepBankDetails.parse_obj(obj)

        _obj = AutoSweepBankDetails.parse_obj({
            "bank_account_details": BankAccountDetails.from_dict(obj.get("bankAccountDetails")) if obj.get("bankAccountDetails") is not None else None,
            "client_registered_address": RegisteredAddress.from_dict(obj.get("clientRegisteredAddress")) if obj.get("clientRegisteredAddress") is not None else None
        })
        return _obj


