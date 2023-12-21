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
from pydantic import BaseModel, Field, StrictStr

class BeneficiaryValidationRequestDTO(BaseModel):
    """
    BeneficiaryValidationRequestDTO
    """
    beneficiary_account_number: Optional[StrictStr] = Field(None, alias="beneficiaryAccountNumber", description="This field accepts the beneficiary account number.")
    beneficiary_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryAccountType")
    beneficiary_bank_code: Optional[StrictStr] = Field(None, alias="beneficiaryBankCode", description="This field accepts the bank code of a beneficiary, for example, bank code for Pakistan will be BHK. Note: This field is mandatory when the destination country is Pakistan (PK).")
    beneficiary_contact_number: Optional[StrictStr] = Field(None, alias="beneficiaryContactNumber")
    beneficiary_country_code: Optional[StrictStr] = Field(None, alias="beneficiaryCountryCode")
    beneficiary_name: Optional[StrictStr] = Field(None, alias="beneficiaryName", description="This field accepts the name of a beneficiary.")
    destination_country: StrictStr = Field(..., alias="destinationCountry", description="This field accepts the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of the destination country.")
    destination_currency: Optional[StrictStr] = Field(None, alias="destinationCurrency")
    payout_method: StrictStr = Field(..., alias="payoutMethod", description="This field can accept the different modes of payout. This field can accept one of the following values: LOCAL PROXY ")
    proxy_type: Optional[StrictStr] = Field(None, alias="proxyType", description="This field indicates the proxy type sent in the payment request.  For SGD-PayNow: The proxy type can be MOBILE, UEN , or NRIC For INR-UPI: The proxy type should be VPA  For MYR-DuitNow: The proxy type can be NRIC, PASSPORT, CORPORATE_REGISTRATION_NUMBER, MOBILE, or ARMY_ID Note : This field is mandatory when the payoutMethod type is PROXY.")
    proxy_value: Optional[StrictStr] = Field(None, alias="proxyValue", description="This field indicates the proxy value such as VPA, UEN, or mobile number etc. Note: This field is mandatory when the payoutMethod type is PROXY The mobile number should include country code.")
    routing_code_type1: Optional[StrictStr] = Field(None, alias="routingCodeType1", description="This field accepts the routing code type 1, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong. This field is Required if the payoutMethod is LOCAL.")
    routing_code_value1: Optional[StrictStr] = Field(None, alias="routingCodeValue1", description="This field accepts the routing code value 1, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE. This field is Required if the payoutMethod is LOCAL.")
    __properties = ["beneficiaryAccountNumber", "beneficiaryAccountType", "beneficiaryBankCode", "beneficiaryContactNumber", "beneficiaryCountryCode", "beneficiaryName", "destinationCountry", "destinationCurrency", "payoutMethod", "proxyType", "proxyValue", "routingCodeType1", "routingCodeValue1"]

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
    def from_json(cls, json_str: str) -> BeneficiaryValidationRequestDTO:
        """Create an instance of BeneficiaryValidationRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BeneficiaryValidationRequestDTO:
        """Create an instance of BeneficiaryValidationRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BeneficiaryValidationRequestDTO.parse_obj(obj)

        _obj = BeneficiaryValidationRequestDTO.parse_obj({
            "beneficiary_account_number": obj.get("beneficiaryAccountNumber"),
            "beneficiary_account_type": obj.get("beneficiaryAccountType"),
            "beneficiary_bank_code": obj.get("beneficiaryBankCode"),
            "beneficiary_contact_number": obj.get("beneficiaryContactNumber"),
            "beneficiary_country_code": obj.get("beneficiaryCountryCode"),
            "beneficiary_name": obj.get("beneficiaryName"),
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "payout_method": obj.get("payoutMethod"),
            "proxy_type": obj.get("proxyType"),
            "proxy_value": obj.get("proxyValue"),
            "routing_code_type1": obj.get("routingCodeType1"),
            "routing_code_value1": obj.get("routingCodeValue1")
        })
        return _obj


