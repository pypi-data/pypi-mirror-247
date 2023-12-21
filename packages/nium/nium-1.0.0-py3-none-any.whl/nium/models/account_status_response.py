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

class AccountStatusResponse(BaseModel):
    """
    AccountStatusResponse
    """
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description=" This field contains the name of the bank which has issued the account linked to this funding instrument.")
    client_hash_id: Optional[StrictStr] = Field(None, alias="clientHashId", description="This field contains the unique 36-character client identifier generated and shared before API handshake.")
    country: Optional[StrictStr] = Field(None, description="This field contains the [ 2-letter ISO-2 country code](https://docs.nium.com/apis/docs/currency-and-country-codes) where the bank account resides.")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp when the funding instrument was added.")
    currency: Optional[StrictStr] = Field(None, description="This field contains the 3-letter [ISO-4217 currency code](https://docs.nium.com/apis/docs/currency-and-country-codes) for the account to be linked.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique 36-character customer identifier generated and shared before API handshake.")
    funding_channel: Optional[StrictStr] = Field(None, alias="fundingChannel", description="The field shows the mode of funding the wallet.")
    funding_instrument_id: Optional[StrictStr] = Field(None, alias="fundingInstrumentId", description="This field contains the unique 36-character funding instrument identifier.")
    masked_account_number: Optional[StrictStr] = Field(None, alias="maskedAccountNumber", description="This field contains the masked bank account number in the format XXXXXXXXXXXX1111.")
    redirect_url: Optional[StrictStr] = Field(None, alias="redirectURL", description="This field contains the URL where the customer is redirected.")
    routing_type: Optional[StrictStr] = Field(None, alias="routingType", description="This field contains the routing code type, for example, 'ACH CODE' for US.")
    routing_value: Optional[StrictStr] = Field(None, alias="routingValue", description="This field contains the routing code value.")
    saved: Optional[StrictBool] = Field(None, description="This flag returns true when the funding instrument is saved. This can return false when funding instrument status is not yet approved.")
    status: Optional[StrictStr] = Field(None, description="This field contains the current status of the funding instrument.")
    status_description: Optional[StrictStr] = Field(None, alias="statusDescription", description="This field contains the additional information of the status response.")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the timestamp when the funding instrument was last updated.")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique 36-character wallet identifier generated and shared before API handshake.")
    __properties = ["bankName", "clientHashId", "country", "createdAt", "currency", "customerHashId", "fundingChannel", "fundingInstrumentId", "maskedAccountNumber", "redirectURL", "routingType", "routingValue", "saved", "status", "statusDescription", "updatedAt", "walletHashId"]

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
    def from_json(cls, json_str: str) -> AccountStatusResponse:
        """Create an instance of AccountStatusResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccountStatusResponse:
        """Create an instance of AccountStatusResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccountStatusResponse.parse_obj(obj)

        _obj = AccountStatusResponse.parse_obj({
            "bank_name": obj.get("bankName"),
            "client_hash_id": obj.get("clientHashId"),
            "country": obj.get("country"),
            "created_at": obj.get("createdAt"),
            "currency": obj.get("currency"),
            "customer_hash_id": obj.get("customerHashId"),
            "funding_channel": obj.get("fundingChannel"),
            "funding_instrument_id": obj.get("fundingInstrumentId"),
            "masked_account_number": obj.get("maskedAccountNumber"),
            "redirect_url": obj.get("redirectURL"),
            "routing_type": obj.get("routingType"),
            "routing_value": obj.get("routingValue"),
            "saved": obj.get("saved"),
            "status": obj.get("status"),
            "status_description": obj.get("statusDescription"),
            "updated_at": obj.get("updatedAt"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


