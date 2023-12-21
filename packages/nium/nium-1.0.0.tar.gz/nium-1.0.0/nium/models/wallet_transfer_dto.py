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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, constr

class WalletTransferDto(BaseModel):
    """
    WalletTransferDto
    """
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field is the amount in source currency which is to be transferred. If destinationAmount is provided, it will take preference over this field.")
    customer_comments: Optional[constr(strict=True, max_length=512)] = Field(None, alias="customerComments", description="This field accepts customer comments for the balance transfer within wallet. Maximum character limit is 512.")
    destination_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="destinationAmount", description="This field is the amount in destination currency which is to be transferred. If provided, amount field is not considered. If this field is skipped, amount is considered in source currency.")
    destination_currency: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="destinationCurrency", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    quote_id: Optional[StrictStr] = Field(None, alias="quoteId")
    source_currency: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="sourceCurrency", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    __properties = ["amount", "customerComments", "destinationAmount", "destinationCurrency", "quoteId", "sourceCurrency"]

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
    def from_json(cls, json_str: str) -> WalletTransferDto:
        """Create an instance of WalletTransferDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletTransferDto:
        """Create an instance of WalletTransferDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletTransferDto.parse_obj(obj)

        _obj = WalletTransferDto.parse_obj({
            "amount": obj.get("amount"),
            "customer_comments": obj.get("customerComments"),
            "destination_amount": obj.get("destinationAmount"),
            "destination_currency": obj.get("destinationCurrency"),
            "quote_id": obj.get("quoteId"),
            "source_currency": obj.get("sourceCurrency")
        })
        return _obj


