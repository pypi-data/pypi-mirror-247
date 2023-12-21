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
from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, validator

class WalletFundingInstrumentsResponseDTO(BaseModel):
    """
    WalletFundingInstrumentsResponseDTO
    """
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description="This field contains the name of the bank which has issued the account linked to this funding instrument.")
    card_bank_name: Optional[StrictStr] = Field(None, alias="cardBankName", description="This field contains the name of the bank which has issued the funding instrument.")
    card_network: Optional[StrictStr] = Field(None, alias="cardNetwork", description="This field contains the card network details. We currently support Visa and MasterCard. It can contain one of the following - visa OR mastercard.")
    card_type: Optional[StrictStr] = Field(None, alias="cardType", description="This field contains the type of funding card. It can contain one of the following - credit OR debit.")
    client_hash_id: Optional[StrictStr] = Field(None, alias="clientHashId", description="This field contains the unique 36-character client identifier generated and shared before API handshake.")
    country: Optional[StrictStr] = Field(None, description="This field contains the Country.")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp of adding funding instrument in YYYY-MM-DD hh:mm:ss format.")
    currency: Optional[StrictStr] = Field(None, description="This field contains the currency.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique 36-character customer identifier generated and shared before API handshake.")
    funding_channel: Optional[StrictStr] = Field(None, alias="fundingChannel", description="This field contains the funding channel of the funding instrument.")
    funding_instrument_id: Optional[StrictStr] = Field(None, alias="fundingInstrumentId", description="This field contains the unique 36-character funding instrument identifier.")
    mask_card_number: Optional[StrictStr] = Field(None, alias="maskCardNumber", description="This field contains the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    masked_account_number: Optional[StrictStr] = Field(None, alias="maskedAccountNumber", description="This field contains the masked account number in the format where only last 4 digits are visible.")
    routing_type: Optional[StrictStr] = Field(None, alias="routingType", description="This field contains the routing type.")
    routing_value: Optional[StrictStr] = Field(None, alias="routingValue", description="This field contains the routing value.")
    saved: Optional[StrictBool] = Field(None, description="This flag indicates whether the funding instrument is saved or not.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status of the funding instrument.")
    three_d_secure_usage: Optional[StrictBool] = Field(None, alias="threeDSecureUsage", description="This flag indicates whether 3DS verification is supported on the card.")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the timestamp of last update to the funding instrument in YYYY-MM-DD hh:mm:ss format")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique 36-character wallet identifier generated and shared before API handshake.")
    __properties = ["bankName", "cardBankName", "cardNetwork", "cardType", "clientHashId", "country", "createdAt", "currency", "customerHashId", "fundingChannel", "fundingInstrumentId", "maskCardNumber", "maskedAccountNumber", "routingType", "routingValue", "saved", "status", "threeDSecureUsage", "updatedAt", "walletHashId"]

    @validator('funding_channel')
    def funding_channel_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('DIRECT_DEBIT'):
            raise ValueError("must be one of enum values ('DIRECT_DEBIT')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED', 'DE_LINKED', 'CANCELLED'):
            raise ValueError("must be one of enum values ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED', 'DE_LINKED', 'CANCELLED')")
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
    def from_json(cls, json_str: str) -> WalletFundingInstrumentsResponseDTO:
        """Create an instance of WalletFundingInstrumentsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletFundingInstrumentsResponseDTO:
        """Create an instance of WalletFundingInstrumentsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletFundingInstrumentsResponseDTO.parse_obj(obj)

        _obj = WalletFundingInstrumentsResponseDTO.parse_obj({
            "bank_name": obj.get("bankName"),
            "card_bank_name": obj.get("cardBankName"),
            "card_network": obj.get("cardNetwork"),
            "card_type": obj.get("cardType"),
            "client_hash_id": obj.get("clientHashId"),
            "country": obj.get("country"),
            "created_at": obj.get("createdAt"),
            "currency": obj.get("currency"),
            "customer_hash_id": obj.get("customerHashId"),
            "funding_channel": obj.get("fundingChannel"),
            "funding_instrument_id": obj.get("fundingInstrumentId"),
            "mask_card_number": obj.get("maskCardNumber"),
            "masked_account_number": obj.get("maskedAccountNumber"),
            "routing_type": obj.get("routingType"),
            "routing_value": obj.get("routingValue"),
            "saved": obj.get("saved"),
            "status": obj.get("status"),
            "three_d_secure_usage": obj.get("threeDSecureUsage"),
            "updated_at": obj.get("updatedAt"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


