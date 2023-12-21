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
from pydantic import BaseModel, Field, StrictStr, validator

class PaymentIdDTO(BaseModel):
    """
    PaymentIdDTO
    """
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description="This field contains the bank name for the paymentId.")
    currency_code: Optional[StrictStr] = Field(None, alias="currencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    unique_payer_id: Optional[StrictStr] = Field(None, alias="uniquePayerId", description="This field contains the unique email Id provided to the customer in addition to uniquePaymentId for supported regions and configuration, or else it will be null, for example, abc12_ca@nium.com.")
    unique_payment_id: Optional[StrictStr] = Field(None, alias="uniquePaymentId", description="This field contains the virtual account number per currency provided to customers for supported regions and configuration, for example, IBAN in EU, virtual account number from Moonova in AU, or else, it will be null.")
    __properties = ["bankName", "currencyCode", "uniquePayerId", "uniquePaymentId"]

    @validator('bank_name')
    def bank_name_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('BOL_LT', 'MONOOVA_AU', 'DBS_HK', 'DBS_SG', 'JPM_AU', 'JPM_SG', 'CB_GB', 'CFSB_US'):
            raise ValueError("must be one of enum values ('BOL_LT', 'MONOOVA_AU', 'DBS_HK', 'DBS_SG', 'JPM_AU', 'JPM_SG', 'CB_GB', 'CFSB_US')")
        return value

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
    def from_json(cls, json_str: str) -> PaymentIdDTO:
        """Create an instance of PaymentIdDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaymentIdDTO:
        """Create an instance of PaymentIdDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentIdDTO.parse_obj(obj)

        _obj = PaymentIdDTO.parse_obj({
            "bank_name": obj.get("bankName"),
            "currency_code": obj.get("currencyCode"),
            "unique_payer_id": obj.get("uniquePayerId"),
            "unique_payment_id": obj.get("uniquePaymentId")
        })
        return _obj


