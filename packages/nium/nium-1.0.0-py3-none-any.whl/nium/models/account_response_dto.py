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

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, validator

class AccountResponseDTO(BaseModel):
    """
    AccountResponseDTO
    """
    account_type: Optional[StrictStr] = Field(None, alias="accountType", description="This field contains the name of the currency pool, for example, \"currency pool\".")
    balance: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field contains the available balance in the pool mentioned in accountType field.")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the date and time of create for an account type.")
    currency: Optional[StrictStr] = Field(None, description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which the balance is specified.")
    is_default: Optional[StrictStr] = Field(None, alias="isDefault", description="This flag will be true only for base currency and false for other currencies.")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the date and time of last update for an account type.")
    __properties = ["accountType", "balance", "createdAt", "currency", "isDefault", "updatedAt"]

    @validator('account_type')
    def account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NIUM_POOL', 'CLIENT_POOL', 'WALLET_POOL', 'INCOME_POOL', 'EXPENSE_POOL', 'RECEIVABLE_POOL', 'UNSETTLED_POOL', 'PAYABLE_POOL', 'SUSPENSE_POOL', 'HOLD_POOL', 'REMIT_POOL', 'NETWORK_POOL'):
            raise ValueError("must be one of enum values ('NIUM_POOL', 'CLIENT_POOL', 'WALLET_POOL', 'INCOME_POOL', 'EXPENSE_POOL', 'RECEIVABLE_POOL', 'UNSETTLED_POOL', 'PAYABLE_POOL', 'SUSPENSE_POOL', 'HOLD_POOL', 'REMIT_POOL', 'NETWORK_POOL')")
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
    def from_json(cls, json_str: str) -> AccountResponseDTO:
        """Create an instance of AccountResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccountResponseDTO:
        """Create an instance of AccountResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccountResponseDTO.parse_obj(obj)

        _obj = AccountResponseDTO.parse_obj({
            "account_type": obj.get("accountType"),
            "balance": obj.get("balance"),
            "created_at": obj.get("createdAt"),
            "currency": obj.get("currency"),
            "is_default": obj.get("isDefault"),
            "updated_at": obj.get("updatedAt")
        })
        return _obj


