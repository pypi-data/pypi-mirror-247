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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, confloat, conint, constr
from nium.models.cancellation_reason import CancellationReason
from nium.models.conversion_status import ConversionStatus

class ConversionCreationResponse(BaseModel):
    """
    ConversionCreationResponse
    """
    id: Optional[StrictStr] = Field(None, description="Unique identifier of the conversion.")
    status: Optional[ConversionStatus] = None
    conversion_time: Optional[datetime] = Field(None, alias="conversionTime", description="Scheduled settlement time in UTC. This is significant for future-dated conversions (e.g., nextDay, 2days). Ensure sufficient funds in the customer's wallet before this time to avoid cancellation and related charges.")
    source_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="sourceCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    destination_currency_code: Optional[constr(strict=True, max_length=3, min_length=3)] = Field(None, alias="destinationCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    source_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="sourceAmount", description="The source amount to be converted to the destination currency.")
    destination_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="destinationAmount", description="The amount needed in the destination currency.")
    quote_id: Optional[StrictStr] = Field(None, alias="quoteId", description="Unique identifier of the quote.")
    net_exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="netExchangeRate", description="Exchange rate with markup to be used for the conversion.")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="exchangeRate", description="Foreign exchange market rate for the currency pair, used as the benchmark for quote calculation.")
    markup_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="markupRate", description="Markup rate applied to the exchange rate for the conversion by Nium.")
    destination_markup_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="destinationMarkupAmount", description="The amount charged in the destination currency as the markup for the conversion.")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="Unique identifier for wallet financial activities used in all Nium reports and dashboards. Refer to [doc](https://docs.nium.com/apis/reference/clienttransactions) for details.")
    customer_comment: Optional[constr(strict=True, max_length=512)] = Field(None, alias="customerComment", description="Free text comment for clients to record and track the conversion.")
    cancellation_fee: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cancellationFee", description="The fee charged when executing the cancellation.")
    cancellation_fee_currency_code: Optional[StrictStr] = Field(None, alias="cancellationFeeCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the cancellation fee.")
    cancellation_reason: Optional[CancellationReason] = Field(None, alias="cancellationReason")
    cancellation_comment: Optional[constr(strict=True, max_length=512)] = Field(None, alias="cancellationComment", description="Free text comment for clients to record and track cancellation of the conversion.")
    cancellation_fee_system_reference_number: Optional[StrictStr] = Field(None, alias="cancellationFeeSystemReferenceNumber", description="Unique identifier for wallet financial activities used in all Nium reports and dashboards. Refer to [doc](https://docs.nium.com/apis/reference/clienttransactions) for details.")
    created_time: Optional[datetime] = Field(None, alias="createdTime", description="Time of creation in UTC.")
    updated_time: Optional[datetime] = Field(None, alias="updatedTime", description="Time of update in UTC.")
    __properties = ["id", "status", "conversionTime", "sourceCurrencyCode", "destinationCurrencyCode", "sourceAmount", "destinationAmount", "quoteId", "netExchangeRate", "exchangeRate", "markupRate", "destinationMarkupAmount", "systemReferenceNumber", "customerComment", "cancellationFee", "cancellationFeeCurrencyCode", "cancellationReason", "cancellationComment", "cancellationFeeSystemReferenceNumber", "createdTime", "updatedTime"]

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
    def from_json(cls, json_str: str) -> ConversionCreationResponse:
        """Create an instance of ConversionCreationResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ConversionCreationResponse:
        """Create an instance of ConversionCreationResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ConversionCreationResponse.parse_obj(obj)

        _obj = ConversionCreationResponse.parse_obj({
            "id": obj.get("id"),
            "status": obj.get("status"),
            "conversion_time": obj.get("conversionTime"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "source_amount": obj.get("sourceAmount"),
            "destination_amount": obj.get("destinationAmount"),
            "quote_id": obj.get("quoteId"),
            "net_exchange_rate": obj.get("netExchangeRate"),
            "exchange_rate": obj.get("exchangeRate"),
            "markup_rate": obj.get("markupRate"),
            "destination_markup_amount": obj.get("destinationMarkupAmount"),
            "system_reference_number": obj.get("systemReferenceNumber"),
            "customer_comment": obj.get("customerComment"),
            "cancellation_fee": obj.get("cancellationFee"),
            "cancellation_fee_currency_code": obj.get("cancellationFeeCurrencyCode"),
            "cancellation_reason": obj.get("cancellationReason"),
            "cancellation_comment": obj.get("cancellationComment"),
            "cancellation_fee_system_reference_number": obj.get("cancellationFeeSystemReferenceNumber"),
            "created_time": obj.get("createdTime"),
            "updated_time": obj.get("updatedTime")
        })
        return _obj


