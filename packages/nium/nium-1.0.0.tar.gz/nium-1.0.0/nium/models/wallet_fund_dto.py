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


from typing import Dict, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, validator
from nium.models.invoice_details import InvoiceDetails

class WalletFundDTO(BaseModel):
    """
    WalletFundDTO
    """
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field is the amount in destination currency which is to be transferred. If the amount is provided, it will take preference over sourceAmount field.")
    country_ip_address: Optional[StrictStr] = Field(None, alias="countryIpAddress", description="The country IP for the device by the customer for initiating the request.")
    currency_map: Optional[Dict[str, Union[StrictFloat, StrictInt]]] = Field(None, alias="currencyMap")
    destination_currency_code: StrictStr = Field(..., alias="destinationCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the destination amount.")
    device_key: Optional[StrictStr] = Field(None, alias="deviceKey", description="Device key")
    funding_channel: StrictStr = Field(..., alias="fundingChannel", description="The value for funding channels can be prefund, bank_transfer, card or direct_debit. Fund wallet using prefund mode is possible as cross-currency. Fund wallet using bank_transfer mode is only possible from SGD to SGD and not cross-currency. direct_debit is only applicable for USA")
    funding_instrument_expiry: Optional[StrictStr] = Field(None, alias="fundingInstrumentExpiry", description="This is base64-encoded expiry date in MMYY format. This is required in case of new card addition.")
    funding_instrument_holder_name: Optional[StrictStr] = Field(None, alias="fundingInstrumentHolderName", description="Name of the card holder as printed on the card. Maximum length of this field is 26 characters. This is required in case of new card.")
    funding_instrument_id: Optional[StrictStr] = Field(None, alias="fundingInstrumentId", description="This field is the unique 36-character funding instrument identifier. The id is a card hash when fundingChannel is cards and applicable only for existing card and not needed for a new card. The id is a bank account identifier when the funding channel is direct debit.")
    funding_instrument_number: Optional[StrictStr] = Field(None, alias="fundingInstrumentNumber", description="This is 16-digit Base64-encoded card number. This is required in case of new card addition.")
    funding_instrument_security_number: Optional[StrictStr] = Field(None, alias="fundingInstrumentSecurityNumber", description="This is base64-encoded 3-digit CVV number. This is required in case of both new and existing card.")
    invoice_details: Optional[InvoiceDetails] = Field(None, alias="invoiceDetails")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress", description="The IP address of the device used by the customer for initiating the request.")
    pocket_name: Optional[StrictStr] = Field(None, alias="pocketName", description="This is the name of the pocket defined under base currency.")
    save: Optional[StrictBool] = Field(None, description="Save funding instrument for future purpose")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId", description="The session Id for the session of the customer for initiating the request.")
    source_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="sourceAmount", description="This field is the amount in source currency that is to be transferred. If amount field is provided, it always takes precedence over sourceAmount")
    source_currency_code: StrictStr = Field(..., alias="sourceCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the source amount.")
    statement_narrative: Optional[StrictStr] = Field(None, alias="statementNarrative", description="This field allows clients to pass a narrative that they want to be displayed in the payer’s account statement when they are pulling funds using Direct Debit. The field value will be truncated at 10 chars for UK and US, and 140 chars for EU.")
    __properties = ["amount", "countryIpAddress", "currencyMap", "destinationCurrencyCode", "deviceKey", "fundingChannel", "fundingInstrumentExpiry", "fundingInstrumentHolderName", "fundingInstrumentId", "fundingInstrumentNumber", "fundingInstrumentSecurityNumber", "invoiceDetails", "ipAddress", "pocketName", "save", "sessionId", "sourceAmount", "sourceCurrencyCode", "statementNarrative"]

    @validator('funding_channel')
    def funding_channel_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('PREFUND', 'BANK_TRANSFER', 'CARD', 'DIRECT_DEBIT', 'FASTER_DIRECT_DEBIT'):
            raise ValueError("must be one of enum values ('PREFUND', 'BANK_TRANSFER', 'CARD', 'DIRECT_DEBIT', 'FASTER_DIRECT_DEBIT')")
        return value

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
    def from_json(cls, json_str: str) -> WalletFundDTO:
        """Create an instance of WalletFundDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of invoice_details
        if self.invoice_details:
            _dict['invoiceDetails'] = self.invoice_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletFundDTO:
        """Create an instance of WalletFundDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletFundDTO.parse_obj(obj)

        _obj = WalletFundDTO.parse_obj({
            "amount": obj.get("amount"),
            "country_ip_address": obj.get("countryIpAddress"),
            "currency_map": obj.get("currencyMap"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "device_key": obj.get("deviceKey"),
            "funding_channel": obj.get("fundingChannel"),
            "funding_instrument_expiry": obj.get("fundingInstrumentExpiry"),
            "funding_instrument_holder_name": obj.get("fundingInstrumentHolderName"),
            "funding_instrument_id": obj.get("fundingInstrumentId"),
            "funding_instrument_number": obj.get("fundingInstrumentNumber"),
            "funding_instrument_security_number": obj.get("fundingInstrumentSecurityNumber"),
            "invoice_details": InvoiceDetails.from_dict(obj.get("invoiceDetails")) if obj.get("invoiceDetails") is not None else None,
            "ip_address": obj.get("ipAddress"),
            "pocket_name": obj.get("pocketName"),
            "save": obj.get("save"),
            "session_id": obj.get("sessionId"),
            "source_amount": obj.get("sourceAmount"),
            "source_currency_code": obj.get("sourceCurrencyCode"),
            "statement_narrative": obj.get("statementNarrative")
        })
        return _obj


