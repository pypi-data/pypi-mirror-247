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
from pydantic import BaseModel, Field, StrictBool, StrictStr, validator
from nium.models.additional_fees_dto import AdditionalFeesDTO
from nium.models.beneficiary import Beneficiary
from nium.models.device_details_dto import DeviceDetailsDTO
from nium.models.payout import Payout
from nium.models.remitter_request_dto import RemitterRequestDTO

class RemittanceTransactionsRequestDTO(BaseModel):
    """
    RemittanceTransactionsRequestDTO
    """
    additional_fees: Optional[AdditionalFeesDTO] = Field(None, alias="additionalFees")
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication).  Note: Either exemption code or authentication is expected if the program's regulatory region is UK or EU. Otherwise, the field should not be used and no value should be passed.")
    beneficiary: Beneficiary = Field(...)
    customer_comments: Optional[StrictStr] = Field(None, alias="customerComments", description="This field is used to add any customer comments.  Maximum character limit is 512.  Note: Special characters are not allowed in this field.")
    device_details: Optional[DeviceDetailsDTO] = Field(None, alias="deviceDetails")
    exemption_code: Optional[StrictStr] = Field(None, alias="exemptionCode", description="This field accepts the reason code for the exemption provided as part of SCA (Strong Customer Authentication). This must be 2 character string and the valid values are as following: 01 - Trusted Beneficiary 04 - Payment to Self Note: Exemption code is expected if authenticationCode is not provided and regulatory region is UK or EU.")
    own_payment: Optional[StrictBool] = Field(None, alias="ownPayment", description="This field applies only to licensed financial institutions. Boolean value 'false' indicates an on-behalf payout request or 'true' indicates a payout executed by the Financial Institution itself. If the field is absent from the request, the default flag is set to 'false'. A valid remitter object is required to be passed for on-behalf payout.")
    payout: Payout = Field(...)
    purpose_code: StrictStr = Field(..., alias="purposeCode", description="This field accepts the purpose code for the payment. Please refer to the [Glossary of Purpose Codes](https://docs.nium.com/baas/transfer-money#glossary-of-purpose-codes): to identify the correct value to be provided.  If purpose code value is not passed then the default value will be IR01802 (Advertising & Public relations-related expenses).  Purpose Code - Description IR001         - Transfer to own account IR002         - Family Maintenance IR003         - Education-related student expenses IR004         - Medical Treatment IR005         - Hotel Accommodation IR006         - Travel IR007         - Utility Bills IR008         - Repayment of Loans IR009         - Tax Payment IR010         - Purchase of Residential Property IR011         - Payment of Property Rental IR012         - Insurance Premium IR013         - Product indemnity insurance IR014         - Insurance Claims Payment IR015         - Mutual Fund Investment IR016         - Investment in Shares IR017         - Donations IR01801       - Information Service Charges IR01802       - Advertising & Public relations-related expenses IR01803       - Royalty fees, trademark fees, patent fees, and copyright fees IR01804       - Fees for brokers, front end fee, commitment fee, guarantee fee and custodian fee IR01805       - Fees for advisors, technical assistance, and academic knowledge, including remuneration for specialists IR01806       - Representative office expenses IR01807       - Construction costs/expenses IR01808       - Transportation fees for goods IR01809       - For payment of exported goods IR01810       - Delivery fees for goods IR01811       - General Goods Trades - Offline trade")
    remitter: Optional[RemitterRequestDTO] = None
    source_of_funds: StrictStr = Field(..., alias="sourceOfFunds", description="This field accepts the source of funds. The possible values are: Salary Personal Savings Personal Wealth Retirement Funds Business Owner/Shareholder Loan Facility Personal AccountCorporate Account")
    __properties = ["additionalFees", "authenticationCode", "beneficiary", "customerComments", "deviceDetails", "exemptionCode", "ownPayment", "payout", "purposeCode", "remitter", "sourceOfFunds"]

    @validator('exemption_code')
    def exemption_code_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('01', '03', '04'):
            raise ValueError("must be one of enum values ('01', '03', '04')")
        return value

    @validator('source_of_funds')
    def source_of_funds_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Salary', 'Personal Savings', 'Personal Wealth', 'Retirement Funds', 'Business Owner/Shareholder', 'Loan Facility', 'Personal Account', 'Corporate Account'):
            raise ValueError("must be one of enum values ('Salary', 'Personal Savings', 'Personal Wealth', 'Retirement Funds', 'Business Owner/Shareholder', 'Loan Facility', 'Personal Account', 'Corporate Account')")
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
    def from_json(cls, json_str: str) -> RemittanceTransactionsRequestDTO:
        """Create an instance of RemittanceTransactionsRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of additional_fees
        if self.additional_fees:
            _dict['additionalFees'] = self.additional_fees.to_dict()
        # override the default output from pydantic by calling `to_dict()` of beneficiary
        if self.beneficiary:
            _dict['beneficiary'] = self.beneficiary.to_dict()
        # override the default output from pydantic by calling `to_dict()` of device_details
        if self.device_details:
            _dict['deviceDetails'] = self.device_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payout
        if self.payout:
            _dict['payout'] = self.payout.to_dict()
        # override the default output from pydantic by calling `to_dict()` of remitter
        if self.remitter:
            _dict['remitter'] = self.remitter.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RemittanceTransactionsRequestDTO:
        """Create an instance of RemittanceTransactionsRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RemittanceTransactionsRequestDTO.parse_obj(obj)

        _obj = RemittanceTransactionsRequestDTO.parse_obj({
            "additional_fees": AdditionalFeesDTO.from_dict(obj.get("additionalFees")) if obj.get("additionalFees") is not None else None,
            "authentication_code": obj.get("authenticationCode"),
            "beneficiary": Beneficiary.from_dict(obj.get("beneficiary")) if obj.get("beneficiary") is not None else None,
            "customer_comments": obj.get("customerComments"),
            "device_details": DeviceDetailsDTO.from_dict(obj.get("deviceDetails")) if obj.get("deviceDetails") is not None else None,
            "exemption_code": obj.get("exemptionCode"),
            "own_payment": obj.get("ownPayment"),
            "payout": Payout.from_dict(obj.get("payout")) if obj.get("payout") is not None else None,
            "purpose_code": obj.get("purposeCode"),
            "remitter": RemitterRequestDTO.from_dict(obj.get("remitter")) if obj.get("remitter") is not None else None,
            "source_of_funds": obj.get("sourceOfFunds")
        })
        return _obj


