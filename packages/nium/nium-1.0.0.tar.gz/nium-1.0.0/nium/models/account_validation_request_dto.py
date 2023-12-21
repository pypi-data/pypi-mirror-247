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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator
from nium.models.bank_routing_info import BankRoutingInfo
from nium.models.beneficiary_account_details_dto import BeneficiaryAccountDetailsDTO

class AccountValidationRequestDTO(BaseModel):
    """
    AccountValidationRequestDTO
    """
    account_number: Optional[StrictStr] = Field(None, alias="accountNumber", description="This field accepts an account number which is to be verified.")
    bank_account_type: StrictStr = Field(..., alias="bankAccountType", description="This field accepts the type of account.")
    bank_code: Optional[StrictStr] = Field(None, alias="bankCode", description="This field accepts the bank code of a beneficiary, for example, bank code for Pakistan will be BHK. Note: This field is mandatory when the destination country is Pakistan (PK).")
    beneficiary: Optional[BeneficiaryAccountDetailsDTO] = None
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry", description="This field accepts the 2-letter [ISO-2 country code](https://docs.nium.com/apis/docs/currency-and-country-codes) of the destination country.")
    destination_currency: StrictStr = Field(..., alias="destinationCurrency", description="This field accepts the 3-letter ISO-3 currency code of the bank account.")
    payout_method: StrictStr = Field(..., alias="payoutMethod", description="This field can accept the different modes of payout.")
    proxy_type: Optional[StrictStr] = Field(None, alias="proxyType", description="This field indicates the proxy type sent in the payment request.  For SGD-PayNow: The proxy type can be MOBILE, UEN , or NRIC For INR-UPI: The proxy type should be VPA  For MYR-DuitNow: The proxy type can be NRIC, PASSPORT, CORPORATE_REGISTRATION_NUMBER, MOBILE, or ARMY_ID Note : This field is mandatory when the payoutMethod type is PROXY.")
    proxy_value: Optional[StrictStr] = Field(None, alias="proxyValue", description="This field indicates the proxy value such as VPA, UEN, or mobile number etc. Note: This field is mandatory when the payoutMethod type is PROXY The mobile number should include country code.")
    routing_info: Optional[conlist(BankRoutingInfo)] = Field(None, alias="routingInfo")
    __properties = ["accountNumber", "bankAccountType", "bankCode", "beneficiary", "destinationCountry", "destinationCurrency", "payoutMethod", "proxyType", "proxyValue", "routingInfo"]

    @validator('bank_account_type')
    def bank_account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('CHECKING', 'SAVING', 'MAESTRA', 'CURRENT'):
            raise ValueError("must be one of enum values ('CHECKING', 'SAVING', 'MAESTRA', 'CURRENT')")
        return value

    @validator('payout_method')
    def payout_method_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('CARD', 'WALLET', 'CASH', 'SWIFT', 'LOCAL', 'PROXY', 'FEDWIRE'):
            raise ValueError("must be one of enum values ('CARD', 'WALLET', 'CASH', 'SWIFT', 'LOCAL', 'PROXY', 'FEDWIRE')")
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
    def from_json(cls, json_str: str) -> AccountValidationRequestDTO:
        """Create an instance of AccountValidationRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of beneficiary
        if self.beneficiary:
            _dict['beneficiary'] = self.beneficiary.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in routing_info (list)
        _items = []
        if self.routing_info:
            for _item in self.routing_info:
                if _item:
                    _items.append(_item.to_dict())
            _dict['routingInfo'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccountValidationRequestDTO:
        """Create an instance of AccountValidationRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccountValidationRequestDTO.parse_obj(obj)

        _obj = AccountValidationRequestDTO.parse_obj({
            "account_number": obj.get("accountNumber"),
            "bank_account_type": obj.get("bankAccountType"),
            "bank_code": obj.get("bankCode"),
            "beneficiary": BeneficiaryAccountDetailsDTO.from_dict(obj.get("beneficiary")) if obj.get("beneficiary") is not None else None,
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "payout_method": obj.get("payoutMethod"),
            "proxy_type": obj.get("proxyType"),
            "proxy_value": obj.get("proxyValue"),
            "routing_info": [BankRoutingInfo.from_dict(_item) for _item in obj.get("routingInfo")] if obj.get("routingInfo") is not None else None
        })
        return _obj


