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
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from nium.models.corporate_customer_response_dto import CorporateCustomerResponseDTO
from nium.models.customer_account_detail import CustomerAccountDetail
from nium.models.individual_customer_response_dto import IndividualCustomerResponseDTO

class CustomerDetailsResponseV2DTO(BaseModel):
    """
    CustomerDetailsResponseV2DTO
    """
    tags: Optional[Dict[str, StrictStr]] = None
    account_details: Optional[conlist(CustomerAccountDetail)] = Field(None, alias="accountDetails")
    block_comment: Optional[StrictStr] = Field(None, alias="blockComment", description="This field contains the comment entered while blocking the customer, if applicable. Otherwise, it contains null.")
    block_reason: Optional[StrictStr] = Field(None, alias="blockReason", description="This field contains the reason for blocking the customer, if applicable. Otherwise, it contains null.")
    block_updated_by: Optional[StrictStr] = Field(None, alias="blockUpdatedBy", description="This field contains the details of the entity updating a customer block/unblock, if applicable. Otherwise, it contains null. The possible values are CLIENT or NIUM.")
    compliance_level: Optional[StrictStr] = Field(None, alias="complianceLevel", description="This field contains the compliance level for the customer. The possible values for customer type INDIVIDUAL are: SCREENING_KYC, SCREENING, SCREENING_KYB. The possible values for customer type CORPORATE is SCREENING_KYB.")
    compliance_remarks: Optional[StrictStr] = Field(None, alias="complianceRemarks", description="This field contains the compliance remarks from Compliance officer, if applicable.")
    compliance_status: Optional[StrictStr] = Field(None, alias="complianceStatus")
    corporate_customer: Optional[CorporateCustomerResponseDTO] = Field(None, alias="corporateCustomer")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp of customer creation in the format YYY-MM-DD hh:mm:ss, for example, 2021-07-29 06:11:43.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId")
    customer_type: Optional[StrictStr] = Field(None, alias="customerType")
    individual_customer: Optional[IndividualCustomerResponseDTO] = Field(None, alias="individualCustomer")
    kyc_mode: Optional[StrictStr] = Field(None, alias="kycMode", description="This field contains the kyc mode  The possible values for customer type INDIVIDUAL are: E_KYC, MANUAL_KYC, SCREENING, EVERIFY_KYC, or NONE.  The possible values for customer type CORPORATE are: KYB or NONE.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains any system-generated compliance comments, if applicable.")
    segment: Optional[StrictStr] = None
    status: Optional[StrictStr] = Field(None, description="This field contains the overall KYC status of the customer")
    terms_and_condition_acceptance_flag: Optional[StrictBool] = Field(None, alias="termsAndConditionAcceptanceFlag", description="This flag denotes that the customer has accepted the Terms and Conditions.")
    terms_and_condition_name: Optional[StrictStr] = Field(None, alias="termsAndConditionName", description="This name that the customer has accepted the Terms and Conditions.")
    terms_and_condition_version_id: Optional[StrictStr] = Field(None, alias="termsAndConditionVersionId", description="This version that the customer has accepted the Terms and Conditions.")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the timestamp of last customer updation in the format YYY-MM-DD hh:mm:ss, for example, 2021-07-29 06:11:43.")
    verification_consent: Optional[StrictBool] = Field(None, alias="verificationConsent", description="This flag contain the customer consent to proceed in case e-Document verification flow is initiated.")
    __properties = ["tags", "accountDetails", "blockComment", "blockReason", "blockUpdatedBy", "complianceLevel", "complianceRemarks", "complianceStatus", "corporateCustomer", "createdAt", "customerHashId", "customerType", "individualCustomer", "kycMode", "remarks", "segment", "status", "termsAndConditionAcceptanceFlag", "termsAndConditionName", "termsAndConditionVersionId", "updatedAt", "verificationConsent"]

    @validator('block_reason')
    def block_reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER'):
            raise ValueError("must be one of enum values ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER')")
        return value

    @validator('block_updated_by')
    def block_updated_by_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NIUM', 'CLIENT'):
            raise ValueError("must be one of enum values ('NIUM', 'CLIENT')")
        return value

    @validator('customer_type')
    def customer_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INDIVIDUAL', 'CORPORATE'):
            raise ValueError("must be one of enum values ('INDIVIDUAL', 'CORPORATE')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Pending', 'Clear', 'Failed', 'Suspended', 'Blocked'):
            raise ValueError("must be one of enum values ('Pending', 'Clear', 'Failed', 'Suspended', 'Blocked')")
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
    def from_json(cls, json_str: str) -> CustomerDetailsResponseV2DTO:
        """Create an instance of CustomerDetailsResponseV2DTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in account_details (list)
        _items = []
        if self.account_details:
            for _item in self.account_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['accountDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of corporate_customer
        if self.corporate_customer:
            _dict['corporateCustomer'] = self.corporate_customer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of individual_customer
        if self.individual_customer:
            _dict['individualCustomer'] = self.individual_customer.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerDetailsResponseV2DTO:
        """Create an instance of CustomerDetailsResponseV2DTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerDetailsResponseV2DTO.parse_obj(obj)

        _obj = CustomerDetailsResponseV2DTO.parse_obj({
            "tags": obj.get("tags"),
            "account_details": [CustomerAccountDetail.from_dict(_item) for _item in obj.get("accountDetails")] if obj.get("accountDetails") is not None else None,
            "block_comment": obj.get("blockComment"),
            "block_reason": obj.get("blockReason"),
            "block_updated_by": obj.get("blockUpdatedBy"),
            "compliance_level": obj.get("complianceLevel"),
            "compliance_remarks": obj.get("complianceRemarks"),
            "compliance_status": obj.get("complianceStatus"),
            "corporate_customer": CorporateCustomerResponseDTO.from_dict(obj.get("corporateCustomer")) if obj.get("corporateCustomer") is not None else None,
            "created_at": obj.get("createdAt"),
            "customer_hash_id": obj.get("customerHashId"),
            "customer_type": obj.get("customerType"),
            "individual_customer": IndividualCustomerResponseDTO.from_dict(obj.get("individualCustomer")) if obj.get("individualCustomer") is not None else None,
            "kyc_mode": obj.get("kycMode"),
            "remarks": obj.get("remarks"),
            "segment": obj.get("segment"),
            "status": obj.get("status"),
            "terms_and_condition_acceptance_flag": obj.get("termsAndConditionAcceptanceFlag"),
            "terms_and_condition_name": obj.get("termsAndConditionName"),
            "terms_and_condition_version_id": obj.get("termsAndConditionVersionId"),
            "updated_at": obj.get("updatedAt"),
            "verification_consent": obj.get("verificationConsent")
        })
        return _obj


