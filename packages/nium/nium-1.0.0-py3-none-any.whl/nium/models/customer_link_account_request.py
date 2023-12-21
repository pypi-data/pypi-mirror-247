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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator
from nium.models.routing_info import RoutingInfo

class CustomerLinkAccountRequest(BaseModel):
    """
    CustomerLinkAccountRequest
    """
    account_number: Optional[StrictStr] = Field(None, alias="accountNumber", description="This field accepts the customer account number or IBAN.")
    country: StrictStr = Field(..., description="This field accepts the [2-letter ISO-2 country code](https://docs.nium.com/apis/docs/currency-and-country-codes) where the bank account resides.")
    currency: StrictStr = Field(..., description="This field accepts the 3-letter [ISO-4217 currency code](https://docs.nium.com/apis/docs/currency-and-country-codes) for the linked account.")
    funding_channel: StrictStr = Field(..., alias="fundingChannel", description="This field indicates the mode of funding a wallet. Adding a new funding instrument is only supported for direct debit.")
    routing_codes: Optional[conlist(RoutingInfo)] = Field(None, alias="routingCodes", description="This field accepts the List of routing code type and value.")
    __properties = ["accountNumber", "country", "currency", "fundingChannel", "routingCodes"]

    @validator('funding_channel')
    def funding_channel_validate_enum(cls, value):
        """Validates the enum"""
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
    def from_json(cls, json_str: str) -> CustomerLinkAccountRequest:
        """Create an instance of CustomerLinkAccountRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in routing_codes (list)
        _items = []
        if self.routing_codes:
            for _item in self.routing_codes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['routingCodes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerLinkAccountRequest:
        """Create an instance of CustomerLinkAccountRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerLinkAccountRequest.parse_obj(obj)

        _obj = CustomerLinkAccountRequest.parse_obj({
            "account_number": obj.get("accountNumber"),
            "country": obj.get("country"),
            "currency": obj.get("currency"),
            "funding_channel": obj.get("fundingChannel"),
            "routing_codes": [RoutingInfo.from_dict(_item) for _item in obj.get("routingCodes")] if obj.get("routingCodes") is not None else None
        })
        return _obj


