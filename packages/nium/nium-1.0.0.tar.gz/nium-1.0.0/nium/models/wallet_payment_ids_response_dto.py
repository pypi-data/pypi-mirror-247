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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictStr, validator

class WalletPaymentIdsResponseDTO(BaseModel):
    """
    WalletPaymentIdsResponseDTO
    """
    tags: Optional[Dict[str, StrictStr]] = None
    account_category: Optional[StrictStr] = Field(None, alias="accountCategory")
    account_name: Optional[StrictStr] = Field(None, alias="accountName")
    account_type: Optional[StrictStr] = Field(None, alias="accountType")
    bank_address: Optional[StrictStr] = Field(None, alias="bankAddress")
    bank_name: Optional[StrictStr] = Field(None, alias="bankName")
    currency_code: Optional[StrictStr] = Field(None, alias="currencyCode")
    full_bank_name: Optional[StrictStr] = Field(None, alias="fullBankName")
    routing_code_type1: Optional[StrictStr] = Field(None, alias="routingCodeType1")
    routing_code_type2: Optional[StrictStr] = Field(None, alias="routingCodeType2")
    routing_code_value1: Optional[StrictStr] = Field(None, alias="routingCodeValue1")
    routing_code_value2: Optional[StrictStr] = Field(None, alias="routingCodeValue2")
    status: Optional[StrictStr] = None
    unique_payer_id: Optional[StrictStr] = Field(None, alias="uniquePayerId")
    unique_payment_id: Optional[StrictStr] = Field(None, alias="uniquePaymentId")
    __properties = ["tags", "accountCategory", "accountName", "accountType", "bankAddress", "bankName", "currencyCode", "fullBankName", "routingCodeType1", "routingCodeType2", "routingCodeValue1", "routingCodeValue2", "status", "uniquePayerId", "uniquePaymentId"]

    @validator('account_category')
    def account_category_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SELF_FUNDING_ACCOUNT', 'COLLECTION_ACCOUNT'):
            raise ValueError("must be one of enum values ('SELF_FUNDING_ACCOUNT', 'COLLECTION_ACCOUNT')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED'):
            raise ValueError("must be one of enum values ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED')")
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
    def from_json(cls, json_str: str) -> WalletPaymentIdsResponseDTO:
        """Create an instance of WalletPaymentIdsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletPaymentIdsResponseDTO:
        """Create an instance of WalletPaymentIdsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletPaymentIdsResponseDTO.parse_obj(obj)

        _obj = WalletPaymentIdsResponseDTO.parse_obj({
            "tags": obj.get("tags"),
            "account_category": obj.get("accountCategory"),
            "account_name": obj.get("accountName"),
            "account_type": obj.get("accountType"),
            "bank_address": obj.get("bankAddress"),
            "bank_name": obj.get("bankName"),
            "currency_code": obj.get("currencyCode"),
            "full_bank_name": obj.get("fullBankName"),
            "routing_code_type1": obj.get("routingCodeType1"),
            "routing_code_type2": obj.get("routingCodeType2"),
            "routing_code_value1": obj.get("routingCodeValue1"),
            "routing_code_value2": obj.get("routingCodeValue2"),
            "status": obj.get("status"),
            "unique_payer_id": obj.get("uniquePayerId"),
            "unique_payment_id": obj.get("uniquePaymentId")
        })
        return _obj


