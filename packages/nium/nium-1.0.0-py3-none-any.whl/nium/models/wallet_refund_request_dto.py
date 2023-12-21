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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, validator

class WalletRefundRequestDTO(BaseModel):
    """
    WalletRefundRequestDTO
    """
    account_name: Optional[StrictStr] = Field(None, alias="accountName", description="This field is needed in case of BANK_TRANSFER to specify the account holder name.")
    account_number: Optional[StrictStr] = Field(None, alias="accountNumber", description="This field is needed in case of BANK_TRANSFER to specify the account number of the receiver.")
    amount: Union[StrictFloat, StrictInt] = Field(..., description="An amount to be transferred.")
    bank_code: Optional[StrictStr] = Field(None, alias="bankCode", description="This field is needed in case of BANK_TRANSFER to specify the bank code for the receiver.")
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description="This field is needed in case of BANK_TRANSFER to specify the bank name for the receiver.")
    comments: Optional[StrictStr] = Field(None, description="This field is for an instruction or a message to support personnel.")
    currency_code: StrictStr = Field(..., alias="currencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the amount")
    pocket_name: Optional[StrictStr] = Field(None, alias="pocketName", description="This is the name of the pocket defined under base currency.")
    refund_mode: StrictStr = Field(..., alias="refundMode", description="The value for refund mode can be CASH or BANK_TRANSFER.")
    __properties = ["accountName", "accountNumber", "amount", "bankCode", "bankName", "comments", "currencyCode", "pocketName", "refundMode"]

    @validator('refund_mode')
    def refund_mode_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('CASH', 'BANK_TRANSFER'):
            raise ValueError("must be one of enum values ('CASH', 'BANK_TRANSFER')")
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
    def from_json(cls, json_str: str) -> WalletRefundRequestDTO:
        """Create an instance of WalletRefundRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletRefundRequestDTO:
        """Create an instance of WalletRefundRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletRefundRequestDTO.parse_obj(obj)

        _obj = WalletRefundRequestDTO.parse_obj({
            "account_name": obj.get("accountName"),
            "account_number": obj.get("accountNumber"),
            "amount": obj.get("amount"),
            "bank_code": obj.get("bankCode"),
            "bank_name": obj.get("bankName"),
            "comments": obj.get("comments"),
            "currency_code": obj.get("currencyCode"),
            "pocket_name": obj.get("pocketName"),
            "refund_mode": obj.get("refundMode")
        })
        return _obj


