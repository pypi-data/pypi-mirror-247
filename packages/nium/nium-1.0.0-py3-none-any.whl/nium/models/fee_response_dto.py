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
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, validator

class FeeResponseDTO(BaseModel):
    """
    FeeResponseDTO
    """
    auth_currency: Optional[StrictStr] = Field(None, alias="authCurrency", description="This field contains the 3-letter [ISO-4217 authorization currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    fee_currency: Optional[StrictStr] = Field(None, alias="feeCurrency", description="This field contains the 3-letter [ISO-4217 fee currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    fee_name: Optional[StrictStr] = Field(None, alias="feeName", description="This field contains the name of the fee or markup.")
    fee_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="feeValue", description="This field contains the actual value of the fee. It can be an amount or percentage.")
    fixed: Optional[StrictBool] = Field(None, description="This field determines if the fee is a fixed amount or a percentage. It is true for a fixed amount and false for a percentage.")
    slab_from: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="slabFrom", description="This field contains the starting point of the slab of transaction amount on which the fee is applicable.")
    slab_to: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="slabTo", description="This field contains the ending point of the slab of transaction amount on which the fee is applicable.")
    status: Optional[StrictStr] = Field(None, description="This field contains the fee status and the possible values are: Active Inactive ")
    threshold_fee_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="thresholdFeeValue", description="This field contains the value of the threshold fee. It can be fixed or percentage.")
    transaction_currency: Optional[StrictStr] = Field(None, alias="transactionCurrency", description="This field contains the 3-letter [ISO-4217 transaction currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    __properties = ["authCurrency", "feeCurrency", "feeName", "feeValue", "fixed", "slabFrom", "slabTo", "status", "thresholdFeeValue", "transactionCurrency"]

    @validator('fee_name')
    def fee_name_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ATM_FEE', 'ECOM_FEE', 'VIR_CARD_FEE', 'PLASTIC_FEE', 'ADDON_CARD_FEE', 'REPLACEMENT_FEE', 'WALLET_REFUND_FEE', 'REMIT_BANK_FEE', 'REMIT_BANK_FEE_SWIFT_BEN', 'REMIT_BANK_FEE_SWIFT_OUR', 'REMIT_BANK_FEE_SWIFT', 'REMIT_CASH_FEE', 'REMIT_WALLET_FEE', 'REMIT_CARD_FEE', 'REMIT_PROXY_FEE', 'REMIT_BANK_FEE_FEDWIRE', 'TRANSACTION_MARKUP', 'FX_MARKUP', 'FX_MARKUP_AUTO_SWEEP', 'FX_MARKUP_AUTO_SWEEP_EOD', 'FX_MARKUP_AUTO_SWEEP_RECEIVE', 'FX_MARKUP_LOCKANDHOLD_1', 'INTERNATIONAL_ATM_FEE', 'ATM_DECLINE_FEE', 'NON_ATM_DECLINE_FEE', 'ACCOUNT_OPENING_FEE', 'ACCOUNT_MAINTENANCE_FEE', 'ACCOUNT_INACTIVE_FEE', 'P2P_FEE', 'WALLET_CREDIT_THIRD_PARTY_FEE', 'WALLET_CREDIT_OFFLINE_FEE', 'WALLET_CREDIT_CARD_FEE', 'WALLET_CREDIT_DIRECT_DEBIT_FEE', 'AUTO_SWEEP_FEE_EOD', 'AUTO_SWEEP_FEE_RECEIVE', 'FX_MARKUP_SETTLE_2DAYS', 'FX_MARKUP_SETTLE_NEXTDAY', 'FX_MARKUP_SETTLE_ENDOFDAY', 'FX_MARKUP_SETTLE_IMMEDIATE', 'FX_MARKUP_LOCK_5MINS', 'FX_MARKUP_LOCK_15MINS', 'FX_MARKUP_LOCK_1HOUR', 'FX_MARKUP_LOCK_4HOURS', 'FX_MARKUP_LOCK_8HOURS', 'FX_MARKUP_LOCK_24HOURS', 'FX_MARKUP_CANCELLATION', 'FX_MARKUP_REVERSAL', 'DOMESTIC_LINKED_CARD_FEE'):
            raise ValueError("must be one of enum values ('ATM_FEE', 'ECOM_FEE', 'VIR_CARD_FEE', 'PLASTIC_FEE', 'ADDON_CARD_FEE', 'REPLACEMENT_FEE', 'WALLET_REFUND_FEE', 'REMIT_BANK_FEE', 'REMIT_BANK_FEE_SWIFT_BEN', 'REMIT_BANK_FEE_SWIFT_OUR', 'REMIT_BANK_FEE_SWIFT', 'REMIT_CASH_FEE', 'REMIT_WALLET_FEE', 'REMIT_CARD_FEE', 'REMIT_PROXY_FEE', 'REMIT_BANK_FEE_FEDWIRE', 'TRANSACTION_MARKUP', 'FX_MARKUP', 'FX_MARKUP_AUTO_SWEEP', 'FX_MARKUP_AUTO_SWEEP_EOD', 'FX_MARKUP_AUTO_SWEEP_RECEIVE', 'FX_MARKUP_LOCKANDHOLD_1', 'INTERNATIONAL_ATM_FEE', 'ATM_DECLINE_FEE', 'NON_ATM_DECLINE_FEE', 'ACCOUNT_OPENING_FEE', 'ACCOUNT_MAINTENANCE_FEE', 'ACCOUNT_INACTIVE_FEE', 'P2P_FEE', 'WALLET_CREDIT_THIRD_PARTY_FEE', 'WALLET_CREDIT_OFFLINE_FEE', 'WALLET_CREDIT_CARD_FEE', 'WALLET_CREDIT_DIRECT_DEBIT_FEE', 'AUTO_SWEEP_FEE_EOD', 'AUTO_SWEEP_FEE_RECEIVE', 'FX_MARKUP_SETTLE_2DAYS', 'FX_MARKUP_SETTLE_NEXTDAY', 'FX_MARKUP_SETTLE_ENDOFDAY', 'FX_MARKUP_SETTLE_IMMEDIATE', 'FX_MARKUP_LOCK_5MINS', 'FX_MARKUP_LOCK_15MINS', 'FX_MARKUP_LOCK_1HOUR', 'FX_MARKUP_LOCK_4HOURS', 'FX_MARKUP_LOCK_8HOURS', 'FX_MARKUP_LOCK_24HOURS', 'FX_MARKUP_CANCELLATION', 'FX_MARKUP_REVERSAL', 'DOMESTIC_LINKED_CARD_FEE')")
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
    def from_json(cls, json_str: str) -> FeeResponseDTO:
        """Create an instance of FeeResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FeeResponseDTO:
        """Create an instance of FeeResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FeeResponseDTO.parse_obj(obj)

        _obj = FeeResponseDTO.parse_obj({
            "auth_currency": obj.get("authCurrency"),
            "fee_currency": obj.get("feeCurrency"),
            "fee_name": obj.get("feeName"),
            "fee_value": obj.get("feeValue"),
            "fixed": obj.get("fixed"),
            "slab_from": obj.get("slabFrom"),
            "slab_to": obj.get("slabTo"),
            "status": obj.get("status"),
            "threshold_fee_value": obj.get("thresholdFeeValue"),
            "transaction_currency": obj.get("transactionCurrency")
        })
        return _obj


