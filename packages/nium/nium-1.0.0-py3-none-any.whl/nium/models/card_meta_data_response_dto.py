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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class CardMetaDataResponseDTO(BaseModel):
    """
    CardMetaDataResponseDTO
    """
    billing_currency_code: Optional[StrictStr] = Field(None, alias="billingCurrencyCode", description="This field contains the 3-letter [ISO-4217 destination currency code](https://www.iso.org/iso-4217-currency-codes.html) for the card billing currency.")
    billing_currency_minor_digits: Optional[StrictStr] = Field(None, alias="billingCurrencyMinorDigits", description="This field contains the number of decimal positions that should be present in any amounts for the requested card's billing currency.")
    card_issuer_country_code: Optional[StrictStr] = Field(None, alias="cardIssuerCountryCode", description="This field indicates the beneficiary card issuer [country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf).")
    card_type_code: Optional[StrictStr] = Field(None, alias="cardTypeCode", description="This field contains the code of the card type, for example, Credit, Debit, Prepaid, Charge, Deferred Debit.")
    fast_funds_indicator: Optional[StrictStr] = Field(None, alias="fastFundsIndicator", description="This field ensures if the card is eligible for fast funds that is if the funds will settle in 30 mins or less. If not eligible then typically fund will settle within 2 business days.")
    is_bank_supported: Optional[StrictBool] = Field(None, alias="isBankSupported", description="This field ensures if the issuer bank is supported by the card type such as Visa or geoswift.")
    is_card_valid: Optional[StrictBool] = Field(None, alias="isCardValid", description="This field ensures if the card details entered is valid or not.")
    issuer_name: Optional[StrictStr] = Field(None, alias="issuerName", description="This field contains the beneficiary card issuer name.")
    online_gambing_block_indicator: Optional[StrictStr] = Field(None, alias="onlineGambingBlockIndicator", description="This code ensures if the card can receive push-payments for online gambling payouts. If the value is \"Y\" then the account cannot receive gambling Push Funds (OCTs). If the value is \"N\" then the account can receive gambling Push Funds (OCTs).")
    push_funds_block_indicator: Optional[StrictStr] = Field(None, alias="pushFundsBlockIndicator", description="This field ensures if the associated card can receive push-to-card disbursements or not.")
    __properties = ["billingCurrencyCode", "billingCurrencyMinorDigits", "cardIssuerCountryCode", "cardTypeCode", "fastFundsIndicator", "isBankSupported", "isCardValid", "issuerName", "onlineGambingBlockIndicator", "pushFundsBlockIndicator"]

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
    def from_json(cls, json_str: str) -> CardMetaDataResponseDTO:
        """Create an instance of CardMetaDataResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardMetaDataResponseDTO:
        """Create an instance of CardMetaDataResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardMetaDataResponseDTO.parse_obj(obj)

        _obj = CardMetaDataResponseDTO.parse_obj({
            "billing_currency_code": obj.get("billingCurrencyCode"),
            "billing_currency_minor_digits": obj.get("billingCurrencyMinorDigits"),
            "card_issuer_country_code": obj.get("cardIssuerCountryCode"),
            "card_type_code": obj.get("cardTypeCode"),
            "fast_funds_indicator": obj.get("fastFundsIndicator"),
            "is_bank_supported": obj.get("isBankSupported"),
            "is_card_valid": obj.get("isCardValid"),
            "issuer_name": obj.get("issuerName"),
            "online_gambing_block_indicator": obj.get("onlineGambingBlockIndicator"),
            "push_funds_block_indicator": obj.get("pushFundsBlockIndicator")
        })
        return _obj


