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

class WalletTransferResponseDto(BaseModel):
    """
    WalletTransferResponseDto
    """
    destination_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="destinationAmount", description="Destination amount is the actual amount credited after deducting Fx and markup.")
    destination_currency_code: Optional[StrictStr] = Field(None, alias="destinationCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="exchangeRate", description="Exchange rate between source and destination currencies.")
    markup_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupAmount", description="Markup amount calculated on the transaction.")
    markup_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupRate", description="Cross-currency markup percentage levied by NIUM.")
    net_exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="netExchangeRate", description="Exchange rate between source and destination currencies derived after accounting for markup. The netExchangeRate should be divided by the scaling factor to fetch the actual exchange rate.")
    scaling_factor: Optional[StrictInt] = Field(None, alias="scalingFactor", description="The netExchangeRate should be divided by the scaling factor to fetch the actual exchange rate.")
    source_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="sourceAmount", description="Source amount is the amount transferred by the customer.")
    source_currency_code: Optional[StrictStr] = Field(None, alias="sourceCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="Unique auth code generated for the transaction by the card issuance platform.")
    __properties = ["destinationAmount", "destinationCurrencyCode", "exchangeRate", "markupAmount", "markupRate", "netExchangeRate", "scalingFactor", "sourceAmount", "sourceCurrencyCode", "systemReferenceNumber"]

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
    def from_json(cls, json_str: str) -> WalletTransferResponseDto:
        """Create an instance of WalletTransferResponseDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletTransferResponseDto:
        """Create an instance of WalletTransferResponseDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletTransferResponseDto.parse_obj(obj)

        _obj = WalletTransferResponseDto.parse_obj({
            "destination_amount": obj.get("destinationAmount"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "exchange_rate": obj.get("exchangeRate"),
            "markup_amount": obj.get("markupAmount"),
            "markup_rate": obj.get("markupRate"),
            "net_exchange_rate": obj.get("netExchangeRate"),
            "scaling_factor": obj.get("scalingFactor"),
            "source_amount": obj.get("sourceAmount"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "system_reference_number": obj.get("systemReferenceNumber")
        })
        return _obj


