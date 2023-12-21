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
from pydantic import BaseModel, Field, StrictStr, validator

class LinkAccountResponse(BaseModel):
    """
    LinkAccountResponse
    """
    country: Optional[StrictStr] = Field(None, description="This field accepts the [2-letter ISO-2 country code ](https://docs.nium.com/apis/docs/currency-and-country-codes) where the bank account resides.")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp when the funding instrument was added.")
    currency: Optional[StrictStr] = Field(None, description="This field accepts the 3-letter [ISO-4217 currency code](https://docs.nium.com/apis/docs/currency-and-country-codes) for the account to be linked.")
    funding_channel: Optional[StrictStr] = Field(None, alias="fundingChannel", description="The field shows the mode of funding the wallet. Only direct debit is supported when adding a new funding instrument.")
    funding_instrument_id: Optional[StrictStr] = Field(None, alias="fundingInstrumentId", description="The unique 36-character alphanumeric identifier of a funding instrument. The ID is a bank account identifier when the funding channel is direct debit.")
    return_url: Optional[StrictStr] = Field(None, alias="returnUrl", description="This field contains the URL where the customer is redirected.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status of the request. The possible values are:   PENDING   FAILED")
    __properties = ["country", "createdAt", "currency", "fundingChannel", "fundingInstrumentId", "returnUrl", "status"]

    @validator('funding_channel')
    def funding_channel_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('DIRECT_DEBIT'):
            raise ValueError("must be one of enum values ('DIRECT_DEBIT')")
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
    def from_json(cls, json_str: str) -> LinkAccountResponse:
        """Create an instance of LinkAccountResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LinkAccountResponse:
        """Create an instance of LinkAccountResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LinkAccountResponse.parse_obj(obj)

        _obj = LinkAccountResponse.parse_obj({
            "country": obj.get("country"),
            "created_at": obj.get("createdAt"),
            "currency": obj.get("currency"),
            "funding_channel": obj.get("fundingChannel"),
            "funding_instrument_id": obj.get("fundingInstrumentId"),
            "return_url": obj.get("returnUrl"),
            "status": obj.get("status")
        })
        return _obj


