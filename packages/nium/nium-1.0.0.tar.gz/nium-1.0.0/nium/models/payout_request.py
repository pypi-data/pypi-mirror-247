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
from pydantic import BaseModel, Field, StrictStr, validator

class PayoutRequest(BaseModel):
    """
    PayoutRequest
    """
    account_number: Optional[StrictStr] = Field(None, description="This field accepts an account number as a payout detail.")
    account_type: Optional[StrictStr] = Field(None, description="This field accepts the type of account. This field is conditional in case of WALLET payout.")
    bank_code: Optional[StrictStr] = Field(None, description="This field accepts the bank code of the payout.")
    bank_name: Optional[StrictStr] = Field(None, description="This field contains the beneficiary bank name.")
    country_code: Optional[StrictStr] = Field(None, description="This field accepts the [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the payout bank.")
    destination_currency: StrictStr = Field(..., description="This field accepts the 3-letter [ISO-4217 destination currency code](https://www.iso.org/iso-4217-currency-codes.html) of the payout as per the destination country from supported corridors.")
    identification_type: Optional[StrictStr] = Field(None, description="This field accepts the type of identification document name for a beneficiary.")
    identification_value: Optional[StrictStr] = Field(None, description="This field accepts an identification document number for the beneficiary.")
    payout_method: StrictStr = Field(..., description="This field accepts the payout method for the remittance payout.")
    proxy_type: Optional[StrictStr] = Field(None, description="This field indicates the proxy type sent in the payment request.  For SGD-PayNow: The proxy type can be MOBILE, UEN, NRIC, or VPA.  For INR-UPI: The proxy type should be VPA. For BRL-PIX: The proxy type can be MOBILE, ID, EMAIL, or RANDOM_KEY For AUD-PayID: The proxy type can be MOBILE, EMAIL, ABN, or ORGANISATION_ID(only domestic payouts are allowed) For MYR-DuitNow: The proxy type can be NRIC, PASSPORT, CORPORATE_REGISTRATION_NUMBER, MOBILE, or ARMY_ID. Note: This field is mandatory when the payout_method type is PROXY")
    proxy_value: Optional[StrictStr] = Field(None, description="This field indicates the proxy value such as VPA, UEN, or mobile number etc. Note: This field is mandatory when the payout_method type is PROXY The mobile number should include country code.")
    routing_code_type_1: Optional[StrictStr] = Field(None, description="This field accepts the routing code type 1, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_type_2: Optional[StrictStr] = Field(None, description="This field accepts the routing code type 2, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_value_1: Optional[StrictStr] = Field(None, description="This field accepts the routing code value 1, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    routing_code_value_2: Optional[StrictStr] = Field(None, description="This field accepts the routing code value 2, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    __properties = ["account_number", "account_type", "bank_code", "bank_name", "country_code", "destination_currency", "identification_type", "identification_value", "payout_method", "proxy_type", "proxy_value", "routing_code_type_1", "routing_code_type_2", "routing_code_value_1", "routing_code_value_2"]

    @validator('account_type')
    def account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Current', 'Saving', 'Maestra', 'Checking'):
            raise ValueError("must be one of enum values ('Current', 'Saving', 'Maestra', 'Checking')")
        return value

    @validator('payout_method')
    def payout_method_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('LOCAL', 'SWIFT', 'WALLET', 'CASH', 'CARD', 'PROXY', 'FEDWIRE'):
            raise ValueError("must be one of enum values ('LOCAL', 'SWIFT', 'WALLET', 'CASH', 'CARD', 'PROXY', 'FEDWIRE')")
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
    def from_json(cls, json_str: str) -> PayoutRequest:
        """Create an instance of PayoutRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PayoutRequest:
        """Create an instance of PayoutRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PayoutRequest.parse_obj(obj)

        _obj = PayoutRequest.parse_obj({
            "account_number": obj.get("account_number"),
            "account_type": obj.get("account_type"),
            "bank_code": obj.get("bank_code"),
            "bank_name": obj.get("bank_name"),
            "country_code": obj.get("country_code"),
            "destination_currency": obj.get("destination_currency"),
            "identification_type": obj.get("identification_type"),
            "identification_value": obj.get("identification_value"),
            "payout_method": obj.get("payout_method"),
            "proxy_type": obj.get("proxy_type"),
            "proxy_value": obj.get("proxy_value"),
            "routing_code_type_1": obj.get("routing_code_type_1"),
            "routing_code_type_2": obj.get("routing_code_type_2"),
            "routing_code_value_1": obj.get("routing_code_value_1"),
            "routing_code_value_2": obj.get("routing_code_value_2")
        })
        return _obj


