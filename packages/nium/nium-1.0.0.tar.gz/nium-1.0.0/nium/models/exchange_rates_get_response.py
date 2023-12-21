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
from typing import List, Optional
from pydantic import BaseModel, Field, conlist, constr
from nium.models.exchange_rate_get_response import ExchangeRateGetResponse
from nium.models.window import Window

class ExchangeRatesGetResponse(BaseModel):
    """
    ExchangeRatesGetResponse
    """
    source_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="sourceCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    destination_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="destinationCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    window: Optional[Window] = None
    exchange_rates: Optional[conlist(ExchangeRateGetResponse)] = Field(None, alias="exchangeRates")
    __properties = ["sourceCurrencyCode", "destinationCurrencyCode", "start", "end", "window", "exchangeRates"]

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
    def from_json(cls, json_str: str) -> ExchangeRatesGetResponse:
        """Create an instance of ExchangeRatesGetResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in exchange_rates (list)
        _items = []
        if self.exchange_rates:
            for _item in self.exchange_rates:
                if _item:
                    _items.append(_item.to_dict())
            _dict['exchangeRates'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExchangeRatesGetResponse:
        """Create an instance of ExchangeRatesGetResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExchangeRatesGetResponse.parse_obj(obj)

        _obj = ExchangeRatesGetResponse.parse_obj({
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "start": obj.get("start"),
            "end": obj.get("end"),
            "window": obj.get("window"),
            "exchange_rates": [ExchangeRateGetResponse.from_dict(_item) for _item in obj.get("exchangeRates")] if obj.get("exchangeRates") is not None else None
        })
        return _obj


