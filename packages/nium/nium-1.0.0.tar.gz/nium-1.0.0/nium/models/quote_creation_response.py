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
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, confloat, conint, constr
from nium.models.conversion_schedule import ConversionSchedule
from nium.models.lock_period import LockPeriod
from nium.models.quote_type import QuoteType

class QuoteCreationResponse(BaseModel):
    """
    QuoteCreationResponse
    """
    id: Optional[StrictStr] = Field(None, description="Unique identifier of the quote.")
    net_exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="netExchangeRate", description="Exchange rate with markup to be used for the conversion.")
    expiry_time: Optional[datetime] = Field(None, alias="expiryTime", description="Expiry time of the quote in UTC.")
    source_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="sourceCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    destination_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="destinationCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    quote_type: Optional[QuoteType] = Field(None, alias="quoteType")
    conversion_schedule: Optional[ConversionSchedule] = Field(None, alias="conversionSchedule")
    lock_period: Optional[LockPeriod] = Field(None, alias="lockPeriod")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="exchangeRate", description="Foreign exchange market rate for the currency pair, used as the benchmark for quote calculation.")
    markup_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupRate", description="Markup rate applied to the exchange rate for the conversion by Nium.")
    ecb_exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="ecbExchangeRate", description="Europe Central Bank's exchange rate for this currency pair, provided only for EU and UK.")
    rate_capture_time: Optional[datetime] = Field(None, alias="rateCaptureTime", description="Time in UTC at which exchange rate was obtained from the rate provider")
    source_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="sourceAmount", description="The source amount to be converted to the destination currency. This value is for reference only and will not be used as the actual conversion amount.")
    destination_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="destinationAmount", description="The amount needed in the destination currency. This value is for reference only and will not be used as the actual conversion amount.")
    destination_markup_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="destinationMarkupAmount", description="The amount charged in the destination currency as the markup for the conversion.")
    created_time: Optional[datetime] = Field(None, alias="createdTime", description="Time of creation in UTC.")
    is_rate_stale: Optional[StrictBool] = Field(None, alias="isRateStale", description="Indicates whether the exchange rate provided is stale. A value of \"true\" suggests that the exchange rate information is no longer current. Clients can use this flag to make informed decisions based on the freshness of the exchange rate.")
    __properties = ["id", "netExchangeRate", "expiryTime", "sourceCurrencyCode", "destinationCurrencyCode", "quoteType", "conversionSchedule", "lockPeriod", "exchangeRate", "markupRate", "ecbExchangeRate", "rateCaptureTime", "sourceAmount", "destinationAmount", "destinationMarkupAmount", "createdTime", "isRateStale"]

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
    def from_json(cls, json_str: str) -> QuoteCreationResponse:
        """Create an instance of QuoteCreationResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> QuoteCreationResponse:
        """Create an instance of QuoteCreationResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QuoteCreationResponse.parse_obj(obj)

        _obj = QuoteCreationResponse.parse_obj({
            "id": obj.get("id"),
            "net_exchange_rate": obj.get("netExchangeRate"),
            "expiry_time": obj.get("expiryTime"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "quote_type": obj.get("quoteType"),
            "conversion_schedule": obj.get("conversionSchedule"),
            "lock_period": obj.get("lockPeriod"),
            "exchange_rate": obj.get("exchangeRate"),
            "markup_rate": obj.get("markupRate"),
            "ecb_exchange_rate": obj.get("ecbExchangeRate"),
            "rate_capture_time": obj.get("rateCaptureTime"),
            "source_amount": obj.get("sourceAmount"),
            "destination_amount": obj.get("destinationAmount"),
            "destination_markup_amount": obj.get("destinationMarkupAmount"),
            "created_time": obj.get("createdTime"),
            "is_rate_stale": obj.get("isRateStale")
        })
        return _obj


