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

class Payment(BaseModel):
    """
    Payment
    """
    creditor_account: Optional[StrictStr] = Field(None, alias="creditorAccount")
    creditor_currency: Optional[StrictStr] = Field(None, alias="creditorCurrency")
    creditor_name: Optional[StrictStr] = Field(None, alias="creditorName")
    debtor_account: Optional[StrictStr] = Field(None, alias="debtorAccount")
    debtor_currency: Optional[StrictStr] = Field(None, alias="debtorCurrency")
    instructed_amount: Optional[StrictStr] = Field(None, alias="instructedAmount")
    instructed_currency: Optional[StrictStr] = Field(None, alias="instructedCurrency")
    __properties = ["creditorAccount", "creditorCurrency", "creditorName", "debtorAccount", "debtorCurrency", "instructedAmount", "instructedCurrency"]

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
    def from_json(cls, json_str: str) -> Payment:
        """Create an instance of Payment from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Payment:
        """Create an instance of Payment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Payment.parse_obj(obj)

        _obj = Payment.parse_obj({
            "creditor_account": obj.get("creditorAccount"),
            "creditor_currency": obj.get("creditorCurrency"),
            "creditor_name": obj.get("creditorName"),
            "debtor_account": obj.get("debtorAccount"),
            "debtor_currency": obj.get("debtorCurrency"),
            "instructed_amount": obj.get("instructedAmount"),
            "instructed_currency": obj.get("instructedCurrency")
        })
        return _obj


