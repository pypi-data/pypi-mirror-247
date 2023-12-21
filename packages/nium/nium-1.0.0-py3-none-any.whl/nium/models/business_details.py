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


from typing import Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.addresses import Addresses
from nium.models.applicant_details import ApplicantDetails
from nium.models.bank_account_details import BankAccountDetails
from nium.models.legal_details import LegalDetails
from nium.models.product_association_details import ProductAssociationDetails
from nium.models.product_document_detail import ProductDocumentDetail
from nium.models.product_partnership_details import ProductPartnershipDetails
from nium.models.product_regulatory_details import ProductRegulatoryDetails
from nium.models.product_tax_details import ProductTaxDetails
from nium.models.stakeholders import Stakeholders

class BusinessDetails(BaseModel):
    """
    BusinessDetails
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This object accepts additional information about the business.  AU: Optional EU: Optional UK: Optional SG: Optional")
    addresses: Optional[Addresses] = None
    applicant_details: Optional[ApplicantDetails] = Field(None, alias="applicantDetails")
    association_details: Optional[ProductAssociationDetails] = Field(None, alias="associationDetails")
    bank_account_details: Optional[BankAccountDetails] = Field(None, alias="bankAccountDetails")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field contains the name of a business.  AU: Required EU: Required UK: Required SG: Required")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the business registration number of the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    business_type: Optional[StrictStr] = Field(None, alias="businessType", description="This field accepts the legal entity type of the business. The supported entity types are: Sole Trader  Private Limited Company Public Company Partnership Limited Liability Partnership Firm Government Body Associations Trust Regulated Trust Unregulated Trust  AU: Required EU: Required UK: Required SG: Required")
    description: Optional[StrictStr] = None
    document_details: Optional[conlist(ProductDocumentDetail)] = Field(None, alias="documentDetails", description="This is an array which accepts the document details for KYB. This field is required only if the documents are being uploaded  AU: Optional EU: Optional UK: Optional SG: Optional")
    former_name: Optional[StrictStr] = Field(None, alias="formerName", description="This field accepts the former name of the new corporate entity to be onboarded.  AU: NA EU: NA UK: NA SG: Optional")
    legal_details: Optional[LegalDetails] = Field(None, alias="legalDetails")
    partnership_details: Optional[ProductPartnershipDetails] = Field(None, alias="partnershipDetails")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field accepts the unique reference ID for the Business Entity provided by client.  AU: Optional EU: Optional UK: Optional SG: Optional")
    regulatory_details: Optional[ProductRegulatoryDetails] = Field(None, alias="regulatoryDetails")
    settlor_name: Optional[StrictStr] = Field(None, alias="settlorName", description="This field accepts the settlor name.  AU: Optional EU: NA UK: NA SG: NA")
    stakeholders: Optional[conlist(Stakeholders)] = Field(None, description="This array accepts the stakeholder details for the new corporate entity to be onboarded. This field is required in case the region is AU and entity type [refer businessDetails.businessType] is one of the following: Sole Trader Unregulated Trust Partnerships Government Body Association  AU: Required EU: Required UK: Required SG: Required")
    stock_symbol: Optional[StrictStr] = Field(None, alias="stockSymbol")
    tax_details: Optional[conlist(ProductTaxDetails)] = Field(None, alias="taxDetails", description="This array accepts the tax details for the new corporate entity to be onboarded.  AU: NA EU: Required UK: NA SG: NA")
    trade_name: Optional[StrictStr] = Field(None, alias="tradeName", description="This field accepts the Trading Name also known as Doing Business As(DBA) name. This field is needed in case the new corporate entity to be onboarded. is doing business with a name other than the registered business name.  AU: Optional EU: Optional UK: Optional SG: Optional")
    trustee_name: Optional[StrictStr] = Field(None, alias="trusteeName", description="This field accepts the full business name of the trustee in case the entity type is a trust. This field is required in case the region is AU and entity type [refer businessDetails.businessType] is a Regulated Trust or an Unregulated Trust.  AU: Optional EU: NA UK: NA SG: Optional")
    website: Optional[StrictStr] = Field(None, description="This field accepts the business website link of the new corporate entity to be onboarded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["additionalInfo", "addresses", "applicantDetails", "associationDetails", "bankAccountDetails", "businessName", "businessRegistrationNumber", "businessType", "description", "documentDetails", "formerName", "legalDetails", "partnershipDetails", "referenceId", "regulatoryDetails", "settlorName", "stakeholders", "stockSymbol", "taxDetails", "tradeName", "trusteeName", "website"]

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
    def from_json(cls, json_str: str) -> BusinessDetails:
        """Create an instance of BusinessDetails from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of bank_account_details
        if self.bank_account_details:
            _dict['bankAccountDetails'] = self.bank_account_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of legal_details
        if self.legal_details:
            _dict['legalDetails'] = self.legal_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of partnership_details
        if self.partnership_details:
            _dict['partnershipDetails'] = self.partnership_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of regulatory_details
        if self.regulatory_details:
            _dict['regulatoryDetails'] = self.regulatory_details.to_dict()
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
    def from_dict(cls, obj: dict) -> BusinessDetails:
        """Create an instance of BusinessDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessDetails.parse_obj(obj)

        _obj = BusinessDetails.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "addresses": Addresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "applicant_details": ApplicantDetails.from_dict(obj.get("applicantDetails")) if obj.get("applicantDetails") is not None else None,
            "association_details": ProductAssociationDetails.from_dict(obj.get("associationDetails")) if obj.get("associationDetails") is not None else None,
            "bank_account_details": BankAccountDetails.from_dict(obj.get("bankAccountDetails")) if obj.get("bankAccountDetails") is not None else None,
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_type": obj.get("businessType"),
            "description": obj.get("description"),
            "document_details": [ProductDocumentDetail.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "former_name": obj.get("formerName"),
            "legal_details": LegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None,
            "partnership_details": ProductPartnershipDetails.from_dict(obj.get("partnershipDetails")) if obj.get("partnershipDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "regulatory_details": ProductRegulatoryDetails.from_dict(obj.get("regulatoryDetails")) if obj.get("regulatoryDetails") is not None else None,
            "settlor_name": obj.get("settlorName"),
            "stakeholders": [Stakeholders.from_dict(_item) for _item in obj.get("stakeholders")] if obj.get("stakeholders") is not None else None,
            "stock_symbol": obj.get("stockSymbol"),
            "tax_details": [ProductTaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "trade_name": obj.get("tradeName"),
            "trustee_name": obj.get("trusteeName"),
            "website": obj.get("website")
        })
        return _obj


