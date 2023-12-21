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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.addresses import Addresses
from nium.models.applicant_details2 import ApplicantDetails2
from nium.models.legal_details import LegalDetails
from nium.models.onboarding_details import OnboardingDetails
from nium.models.product_association_details import ProductAssociationDetails
from nium.models.product_document_detail import ProductDocumentDetail
from nium.models.product_partnership_details import ProductPartnershipDetails
from nium.models.product_regulatory_details import ProductRegulatoryDetails
from nium.models.product_tax_details import ProductTaxDetails
from nium.models.revenue_info import RevenueInfo
from nium.models.stakeholders2 import Stakeholders2

class BusinessDetails2(BaseModel):
    """
    BusinessDetails2
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This object accepts additional information about the business.")
    addresses: Optional[Addresses] = None
    applicant_details: Optional[ApplicantDetails2] = Field(None, alias="applicantDetails")
    association_details: Optional[ProductAssociationDetails] = Field(None, alias="associationDetails")
    business_in_other_countries: Optional[conlist(Dict[str, Any])] = Field(None, alias="businessInOtherCountries")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field accepts the registered business name of the corporate entity.")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the business registration number of the corporate entity.")
    business_type: Optional[StrictStr] = Field(None, alias="businessType")
    description: Optional[StrictStr] = None
    document_details: Optional[ProductDocumentDetail] = Field(None, alias="documentDetails")
    legal_details: Optional[LegalDetails] = Field(None, alias="legalDetails")
    onboarding_details: Optional[OnboardingDetails] = Field(None, alias="onboardingDetails")
    partnership_details: Optional[ProductPartnershipDetails] = Field(None, alias="partnershipDetails")
    purpose_code: Optional[StrictStr] = Field(None, alias="purposeCode")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field accepts the reference Id of the business information for which the RFI is raised.")
    regulatory_details: Optional[ProductRegulatoryDetails] = Field(None, alias="regulatoryDetails")
    revenue_info: Optional[RevenueInfo] = Field(None, alias="revenueInfo")
    settlor_name: Optional[StrictStr] = Field(None, alias="settlorName", description="This field accepts the settlor name.")
    stakeholders: Optional[conlist(Stakeholders2)] = Field(None, description="This array accepts the stakeholder details for the corporate entity.")
    tax_details: Optional[conlist(ProductTaxDetails)] = Field(None, alias="taxDetails")
    ticker: Optional[StrictStr] = None
    trade_name: Optional[StrictStr] = Field(None, alias="tradeName", description="This field accepts the Trading Name also known as Doing Business As(DBA) name.")
    trustee_name: Optional[StrictStr] = Field(None, alias="trusteeName", description="This field accepts the full business name of the trustee in case the entity type is a trust.")
    website: Optional[StrictStr] = None
    __properties = ["additionalInfo", "addresses", "applicantDetails", "associationDetails", "businessInOtherCountries", "businessName", "businessRegistrationNumber", "businessType", "description", "documentDetails", "legalDetails", "onboardingDetails", "partnershipDetails", "purposeCode", "referenceId", "regulatoryDetails", "revenueInfo", "settlorName", "stakeholders", "taxDetails", "ticker", "tradeName", "trusteeName", "website"]

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
    def from_json(cls, json_str: str) -> BusinessDetails2:
        """Create an instance of BusinessDetails2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of addresses
        if self.addresses:
            _dict['addresses'] = self.addresses.to_dict()
        # override the default output from pydantic by calling `to_dict()` of applicant_details
        if self.applicant_details:
            _dict['applicantDetails'] = self.applicant_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of association_details
        if self.association_details:
            _dict['associationDetails'] = self.association_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of document_details
        if self.document_details:
            _dict['documentDetails'] = self.document_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of legal_details
        if self.legal_details:
            _dict['legalDetails'] = self.legal_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of onboarding_details
        if self.onboarding_details:
            _dict['onboardingDetails'] = self.onboarding_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of partnership_details
        if self.partnership_details:
            _dict['partnershipDetails'] = self.partnership_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of regulatory_details
        if self.regulatory_details:
            _dict['regulatoryDetails'] = self.regulatory_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of revenue_info
        if self.revenue_info:
            _dict['revenueInfo'] = self.revenue_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in stakeholders (list)
        _items = []
        if self.stakeholders:
            for _item in self.stakeholders:
                if _item:
                    _items.append(_item.to_dict())
            _dict['stakeholders'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessDetails2:
        """Create an instance of BusinessDetails2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessDetails2.parse_obj(obj)

        _obj = BusinessDetails2.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "addresses": Addresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "applicant_details": ApplicantDetails2.from_dict(obj.get("applicantDetails")) if obj.get("applicantDetails") is not None else None,
            "association_details": ProductAssociationDetails.from_dict(obj.get("associationDetails")) if obj.get("associationDetails") is not None else None,
            "business_in_other_countries": obj.get("businessInOtherCountries"),
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_type": obj.get("businessType"),
            "description": obj.get("description"),
            "document_details": ProductDocumentDetail.from_dict(obj.get("documentDetails")) if obj.get("documentDetails") is not None else None,
            "legal_details": LegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None,
            "onboarding_details": OnboardingDetails.from_dict(obj.get("onboardingDetails")) if obj.get("onboardingDetails") is not None else None,
            "partnership_details": ProductPartnershipDetails.from_dict(obj.get("partnershipDetails")) if obj.get("partnershipDetails") is not None else None,
            "purpose_code": obj.get("purposeCode"),
            "reference_id": obj.get("referenceId"),
            "regulatory_details": ProductRegulatoryDetails.from_dict(obj.get("regulatoryDetails")) if obj.get("regulatoryDetails") is not None else None,
            "revenue_info": RevenueInfo.from_dict(obj.get("revenueInfo")) if obj.get("revenueInfo") is not None else None,
            "settlor_name": obj.get("settlorName"),
            "stakeholders": [Stakeholders2.from_dict(_item) for _item in obj.get("stakeholders")] if obj.get("stakeholders") is not None else None,
            "tax_details": [ProductTaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "ticker": obj.get("ticker"),
            "trade_name": obj.get("tradeName"),
            "trustee_name": obj.get("trusteeName"),
            "website": obj.get("website")
        })
        return _obj


