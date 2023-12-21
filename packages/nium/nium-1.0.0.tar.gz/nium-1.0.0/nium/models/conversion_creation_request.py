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
from pydantic import BaseModel, Field, StrictStr, confloat, conint, constr

class ConversionCreationRequest(BaseModel):
    """
    ConversionCreationRequest
    """
    customer_comment: Optional[constr(strict=True, max_length=512)] = Field(None, alias="customerComment", description="Free text comment for clients to record and track the conversion.")
    quote_id: Optional[StrictStr] = Field(None, alias="quoteId", description="Unique identifier of the quote.")
    source_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="sourceCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    destination_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="destinationCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    source_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="sourceAmount", description="The source amount to be converted to the destination currency.")
    destination_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="destinationAmount", description="The amount needed in the destination currency.")
    __properties = ["customerComment", "quoteId", "sourceCurrencyCode", "destinationCurrencyCode", "sourceAmount", "destinationAmount"]

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
    def from_json(cls, json_str: str) -> ConversionCreationRequest:
        """Create an instance of ConversionCreationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ConversionCreationRequest:
        """Create an instance of ConversionCreationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ConversionCreationRequest.parse_obj(obj)

        _obj = ConversionCreationRequest.parse_obj({
            "customer_comment": obj.get("customerComment"),
            "quote_id": obj.get("quoteId"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "source_amount": obj.get("sourceAmount"),
            "destination_amount": obj.get("destinationAmount")
        })
        return _obj


