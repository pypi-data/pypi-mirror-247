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
from pydantic import BaseModel, Field, confloat, conint, constr
from nium.models.conversion_schedule import ConversionSchedule
from nium.models.lock_period import LockPeriod
from nium.models.quote_type import QuoteType

class QuoteCreationRequest(BaseModel):
    """
    QuoteCreationRequest
    """
    source_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="sourceAmount", description="The source amount to be converted to the destination currency. This value is for reference only and will not be used as the actual conversion amount.")
    destination_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="destinationAmount", description="The amount needed in the destination currency. This value is for reference only and will not be used as the actual conversion amount.")
    source_currency_code: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="sourceCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    destination_currency_code: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="destinationCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    quote_type: QuoteType = Field(..., alias="quoteType")
    conversion_schedule: Optional[ConversionSchedule] = Field(None, alias="conversionSchedule")
    lock_period: Optional[LockPeriod] = Field(None, alias="lockPeriod")
    __properties = ["sourceAmount", "destinationAmount", "sourceCurrencyCode", "destinationCurrencyCode", "quoteType", "conversionSchedule", "lockPeriod"]

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
    def from_json(cls, json_str: str) -> QuoteCreationRequest:
        """Create an instance of QuoteCreationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> QuoteCreationRequest:
        """Create an instance of QuoteCreationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QuoteCreationRequest.parse_obj(obj)

        _obj = QuoteCreationRequest.parse_obj({
            "source_amount": obj.get("sourceAmount"),
            "destination_amount": obj.get("destinationAmount"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "quote_type": obj.get("quoteType"),
            "conversion_schedule": obj.get("conversionSchedule"),
            "lock_period": obj.get("lockPeriod")
        })
        return _obj


