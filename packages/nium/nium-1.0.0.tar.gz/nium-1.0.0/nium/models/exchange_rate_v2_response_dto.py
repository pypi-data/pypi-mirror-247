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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class ExchangeRateV2ResponseDto(BaseModel):
    """
    ExchangeRateV2ResponseDto
    """
    destination_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="destinationAmount", description="The credited amount.")
    destination_currency_code: Optional[StrictStr] = Field(None, alias="destinationCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    ecb_fx_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="ecbFxRate", description="The ecb exchange rate fetched for the conversion. This field is only applicable for EU and UK.")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="exchangeRate", description="The exchange rate fetched for the conversion.")
    expiry_date: Optional[StrictStr] = Field(None, alias="expiryDate", description="Timestamp till which the quoted rate is valid. The timezone is UTC +00.")
    markup_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupAmount", description="In case source or destination amount is provided the markup amount will be calculated using markupRate.")
    markup_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupRate", description="This is the markup rate charged by NIUM.")
    net_exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="netExchangeRate", description="This is exchangeRate subtracted by the markupRate.")
    quote_id: Optional[StrictStr] = Field(None, alias="quoteId", description="Unique quote Id for the exchange rate.")
    scaling_factor: Optional[StrictInt] = Field(None, alias="scalingFactor", description="The netExchangeRate should be divided by the scaling factor to fetch the actual exchange rate.")
    source_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="sourceAmount", description="An amount to be converted.")
    source_currency_code: Optional[StrictStr] = Field(None, alias="sourceCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    __properties = ["destinationAmount", "destinationCurrencyCode", "ecbFxRate", "exchangeRate", "expiryDate", "markupAmount", "markupRate", "netExchangeRate", "quoteId", "scalingFactor", "sourceAmount", "sourceCurrencyCode"]

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
    def from_json(cls, json_str: str) -> ExchangeRateV2ResponseDto:
        """Create an instance of ExchangeRateV2ResponseDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExchangeRateV2ResponseDto:
        """Create an instance of ExchangeRateV2ResponseDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExchangeRateV2ResponseDto.parse_obj(obj)

        _obj = ExchangeRateV2ResponseDto.parse_obj({
            "destination_amount": obj.get("destinationAmount"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "ecb_fx_rate": obj.get("ecbFxRate"),
            "exchange_rate": obj.get("exchangeRate"),
            "expiry_date": obj.get("expiryDate"),
            "markup_amount": obj.get("markupAmount"),
            "markup_rate": obj.get("markupRate"),
            "net_exchange_rate": obj.get("netExchangeRate"),
            "quote_id": obj.get("quoteId"),
            "scaling_factor": obj.get("scalingFactor"),
            "source_amount": obj.get("sourceAmount"),
            "source_currency_code": obj.get("sourceCurrencyCode")
        })
        return _obj


