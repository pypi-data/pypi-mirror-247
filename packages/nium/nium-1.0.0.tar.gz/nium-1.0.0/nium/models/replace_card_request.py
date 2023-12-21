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
from pydantic import BaseModel, Field, StrictStr, constr

class ReplaceCardRequest(BaseModel):
    """
    A card can be replaced using the Replace Card API only if it is permanently blocked. A permanently blocked card cannot be replaced on the same date as date of issuance. For example, a customer issued a card today and request to block the card permanently, on the same day. However, a customer may not call the Replace Card API to issue a replacement on the same date.  # noqa: E501
    """
    card_expiry: Optional[StrictStr] = Field(None, alias="cardExpiry", description="Expiry date to be set for virtual and virtual upgraded to physical cards. This field is not required for a physical card.")
    card_fee_currency_code: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="cardFeeCurrencyCode", description="This field accepts 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which the client wants to levy the card issuance fee.")
    plastic_id: Optional[StrictStr] = Field(None, alias="plasticId")
    __properties = ["cardExpiry", "cardFeeCurrencyCode", "plasticId"]

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
    def from_json(cls, json_str: str) -> ReplaceCardRequest:
        """Create an instance of ReplaceCardRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReplaceCardRequest:
        """Create an instance of ReplaceCardRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReplaceCardRequest.parse_obj(obj)

        _obj = ReplaceCardRequest.parse_obj({
            "card_expiry": obj.get("cardExpiry"),
            "card_fee_currency_code": obj.get("cardFeeCurrencyCode"),
            "plastic_id": obj.get("plasticId")
        })
        return _obj


