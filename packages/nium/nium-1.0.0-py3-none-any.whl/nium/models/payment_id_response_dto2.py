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

class PaymentIdResponseDTO2(BaseModel):
    """
    PaymentIdResponseDTO2
    """
    bank_name: Optional[StrictStr] = Field(None, alias="bankName")
    currency_code: Optional[StrictStr] = Field(None, alias="currencyCode")
    unique_payer_id: Optional[StrictStr] = Field(None, alias="uniquePayerId")
    unique_payment_id: Optional[StrictStr] = Field(None, alias="uniquePaymentId")
    __properties = ["bankName", "currencyCode", "uniquePayerId", "uniquePaymentId"]

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
    def from_json(cls, json_str: str) -> PaymentIdResponseDTO2:
        """Create an instance of PaymentIdResponseDTO2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaymentIdResponseDTO2:
        """Create an instance of PaymentIdResponseDTO2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentIdResponseDTO2.parse_obj(obj)

        _obj = PaymentIdResponseDTO2.parse_obj({
            "bank_name": obj.get("bankName"),
            "currency_code": obj.get("currencyCode"),
            "unique_payer_id": obj.get("uniquePayerId"),
            "unique_payment_id": obj.get("uniquePaymentId")
        })
        return _obj


