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

class ReferenceRateResponseDto(BaseModel):
    """
    ReferenceRateResponseDto
    """
    as_of_date: Optional[StrictStr] = Field(None, alias="asOfDate", description="This field contains the date on which fx rate has to be calculated. The timezone is UTC +00.")
    card_scheme: Optional[StrictStr] = Field(None, alias="cardScheme", description="This field contains the card scheme provider name.")
    card_scheme_fx_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cardSchemeFxRate", description="This is the fx rate from cards scheme.")
    card_scheme_fx_rate_last_updated_at: Optional[StrictStr] = Field(None, alias="cardSchemeFxRateLastUpdatedAt", description="Last updated timestamp of card scheme fx rate. The timezone is UTC +00.")
    card_scheme_fx_rate_with_fx_markup: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cardSchemeFxRateWithFxMarkup", description="This is the cards scheme fx rate with fx markup.")
    card_scheme_markup_over_ecb: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cardSchemeMarkupOverEcb", description="The markup rate over ecb rate. Available for currencies listed in [Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)")
    ecb_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="ecbRate", description="The ecb exchange rate fetched for the conversion. Available for currencies listed in [Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)")
    ecb_rate_last_updated_at: Optional[StrictStr] = Field(None, alias="ecbRateLastUpdatedAt", description="Last updated timestamp of ecb rate. The timezone is UTC +00. Available for currencies listed in [Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)")
    from_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fromAmount", description="An amount to be converted.")
    from_currency: Optional[StrictStr] = Field(None, alias="fromCurrency", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    fx_markup: Optional[Union[StrictFloat, StrictInt]] = Field(0, alias="fxMarkup", description="This is the fx markup rate.")
    to_amount_with_ecb_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="toAmountWithEcbRate", description="The ecb exchange rate with to amount.")
    to_amount_with_transaction_fee_and_fx_markup: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="toAmountWithTransactionFeeAndFxMarkup", description="The amount with transaction fee and fx markup rate.")
    to_currency: Optional[StrictStr] = Field(None, alias="toCurrency", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    transaction_fee: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="transactionFee", description="This is the transaction fee.")
    __properties = ["asOfDate", "cardScheme", "cardSchemeFxRate", "cardSchemeFxRateLastUpdatedAt", "cardSchemeFxRateWithFxMarkup", "cardSchemeMarkupOverEcb", "ecbRate", "ecbRateLastUpdatedAt", "fromAmount", "fromCurrency", "fxMarkup", "toAmountWithEcbRate", "toAmountWithTransactionFeeAndFxMarkup", "toCurrency", "transactionFee"]

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
    def from_json(cls, json_str: str) -> ReferenceRateResponseDto:
        """Create an instance of ReferenceRateResponseDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReferenceRateResponseDto:
        """Create an instance of ReferenceRateResponseDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReferenceRateResponseDto.parse_obj(obj)

        _obj = ReferenceRateResponseDto.parse_obj({
            "as_of_date": obj.get("asOfDate"),
            "card_scheme": obj.get("cardScheme"),
            "card_scheme_fx_rate": obj.get("cardSchemeFxRate"),
            "card_scheme_fx_rate_last_updated_at": obj.get("cardSchemeFxRateLastUpdatedAt"),
            "card_scheme_fx_rate_with_fx_markup": obj.get("cardSchemeFxRateWithFxMarkup"),
            "card_scheme_markup_over_ecb": obj.get("cardSchemeMarkupOverEcb"),
            "ecb_rate": obj.get("ecbRate"),
            "ecb_rate_last_updated_at": obj.get("ecbRateLastUpdatedAt"),
            "from_amount": obj.get("fromAmount"),
            "from_currency": obj.get("fromCurrency"),
            "fx_markup": obj.get("fxMarkup") if obj.get("fxMarkup") is not None else 0,
            "to_amount_with_ecb_rate": obj.get("toAmountWithEcbRate"),
            "to_amount_with_transaction_fee_and_fx_markup": obj.get("toAmountWithTransactionFeeAndFxMarkup"),
            "to_currency": obj.get("toCurrency"),
            "transaction_fee": obj.get("transactionFee")
        })
        return _obj


