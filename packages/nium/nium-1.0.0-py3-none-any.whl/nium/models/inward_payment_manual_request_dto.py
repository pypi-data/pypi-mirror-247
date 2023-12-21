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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, validator

class InwardPaymentManualRequestDTO(BaseModel):
    """
    InwardPaymentManualRequestDTO
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This object accepts the additional information")
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field contains the amount.")
    bank_reference_number: Optional[StrictStr] = Field(None, alias="bankReferenceNumber", description="This field contains the bank reference number")
    bank_source: Optional[StrictStr] = Field(None, alias="bankSource", description="This field contains the source of payment/fund.")
    country: Optional[StrictStr] = Field(None, description="This field contains the country.")
    currency: Optional[StrictStr] = Field(None, description="This field contains the 3-letter currency code.")
    icc_expiry: Optional[StrictStr] = Field(None, alias="iccExpiry", description="This field contains the expiry time for ICC.")
    instruction_type: Optional[StrictStr] = Field(None, alias="instructionType", description="This field contains the payment instruction type")
    narrative: Optional[StrictStr] = Field(None, description="This field contains the narrative.")
    remitter_account_number: Optional[StrictStr] = Field(None, alias="remitterAccountNumber", description="This field contains the remitter account number.")
    remitter_bank_code: Optional[StrictStr] = Field(None, alias="remitterBankCode", description="This field contains the remitter bank code.")
    remitter_bank_name: Optional[StrictStr] = Field(None, alias="remitterBankName", description="This field contains the remitter bank name.")
    remitter_name: Optional[StrictStr] = Field(None, alias="remitterName", description="This field contains the remitter name.")
    remitter_name_local_language: Optional[StrictStr] = Field(None, alias="remitterNameLocalLanguage", description="This field contains the remitter name local language.")
    transaction_id: Optional[StrictStr] = Field(None, alias="transactionId", description="This field contains the transaction reference number/ID.")
    transaction_source: Optional[StrictStr] = Field(None, alias="transactionSource", description="This field contains the ICC transaction source.")
    type: Optional[StrictStr] = Field(None, description="This field contains the ICC entry type.")
    virtual_account_number: Optional[StrictStr] = Field(None, alias="virtualAccountNumber", description="This field contains the virtual account number.")
    __properties = ["additionalInfo", "amount", "bankReferenceNumber", "bankSource", "country", "currency", "iccExpiry", "instructionType", "narrative", "remitterAccountNumber", "remitterBankCode", "remitterBankName", "remitterName", "remitterNameLocalLanguage", "transactionId", "transactionSource", "type", "virtualAccountNumber"]

    @validator('bank_source')
    def bank_source_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('DBS_HK', 'DBS_SG', 'JPM_SG', 'JPM_AU', 'JPM_UK', 'MONOOVA_AU', 'BOL_LT', 'CB_GB', 'CFSB_US', 'BARCLAYS', 'CITI_SG', 'CITI_MX', 'CFSB_USINTL', 'GMO_JP', 'NETBANK_PH', 'GOCARDLESS', 'DIRECTFAST_SG', 'BANKINGCIRCLE_PL'):
            raise ValueError("must be one of enum values ('DBS_HK', 'DBS_SG', 'JPM_SG', 'JPM_AU', 'JPM_UK', 'MONOOVA_AU', 'BOL_LT', 'CB_GB', 'CFSB_US', 'BARCLAYS', 'CITI_SG', 'CITI_MX', 'CFSB_USINTL', 'GMO_JP', 'NETBANK_PH', 'GOCARDLESS', 'DIRECTFAST_SG', 'BANKINGCIRCLE_PL')")
        return value

    @validator('currency')
    def currency_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SGD', 'AUD', 'EUR', 'HKD', 'USD', 'GBP', 'AED', 'CAD', 'CHF', 'CZK', 'DKK', 'HUF', 'ILS', 'MXN', 'NOK', 'NZD', 'PLN', 'RON', 'RUB', 'SEK', 'ZAR', 'CNY', 'JPY', 'THB', 'TRY', 'PHP'):
            raise ValueError("must be one of enum values ('SGD', 'AUD', 'EUR', 'HKD', 'USD', 'GBP', 'AED', 'CAD', 'CHF', 'CZK', 'DKK', 'HUF', 'ILS', 'MXN', 'NOK', 'NZD', 'PLN', 'RON', 'RUB', 'SEK', 'ZAR', 'CNY', 'JPY', 'THB', 'TRY', 'PHP')")
        return value

    @validator('instruction_type')
    def instruction_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INQUIRY', 'PROCESS'):
            raise ValueError("must be one of enum values ('INQUIRY', 'PROCESS')")
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
    def from_json(cls, json_str: str) -> InwardPaymentManualRequestDTO:
        """Create an instance of InwardPaymentManualRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InwardPaymentManualRequestDTO:
        """Create an instance of InwardPaymentManualRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InwardPaymentManualRequestDTO.parse_obj(obj)

        _obj = InwardPaymentManualRequestDTO.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "amount": obj.get("amount"),
            "bank_reference_number": obj.get("bankReferenceNumber"),
            "bank_source": obj.get("bankSource"),
            "country": obj.get("country"),
            "currency": obj.get("currency"),
            "icc_expiry": obj.get("iccExpiry"),
            "instruction_type": obj.get("instructionType"),
            "narrative": obj.get("narrative"),
            "remitter_account_number": obj.get("remitterAccountNumber"),
            "remitter_bank_code": obj.get("remitterBankCode"),
            "remitter_bank_name": obj.get("remitterBankName"),
            "remitter_name": obj.get("remitterName"),
            "remitter_name_local_language": obj.get("remitterNameLocalLanguage"),
            "transaction_id": obj.get("transactionId"),
            "transaction_source": obj.get("transactionSource"),
            "type": obj.get("type"),
            "virtual_account_number": obj.get("virtualAccountNumber")
        })
        return _obj


