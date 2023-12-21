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
from nium.models.contact_details import ContactDetails
from nium.models.product_address import ProductAddress
from nium.models.product_document_detail import ProductDocumentDetail
from nium.models.product_professional_details import ProductProfessionalDetails
from nium.models.product_tax_details import ProductTaxDetails

class StakeholderDetails2(BaseModel):
    """
    StakeholderDetails2
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo")
    address: Optional[ProductAddress] = None
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry")
    contact_details: Optional[ContactDetails] = Field(None, alias="contactDetails")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field accepts the date of birth of the stakeholder.")
    document_details: Optional[ProductDocumentDetail] = Field(None, alias="documentDetails")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field accepts the first name of the stakeholder.")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the stakeholder. The acceptable values are: Male Female")
    is_primary_applicant: Optional[StrictStr] = Field(None, alias="isPrimaryApplicant")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field accepts the last name of the stakeholder.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of the stakeholder.")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the nationality of the stakeholder.")
    professional_details: Optional[conlist(ProductProfessionalDetails)] = Field(None, alias="professionalDetails", description="This array accepts the professional details of the stakeholder.")
    source_of_funds: Optional[StrictStr] = Field(None, alias="sourceOfFunds")
    tax_details: Optional[conlist(ProductTaxDetails)] = Field(None, alias="taxDetails", description="This an array which accepts the tax details.")
    title: Optional[StrictStr] = None
    __properties = ["additionalInfo", "address", "birthCountry", "contactDetails", "dateOfBirth", "documentDetails", "firstName", "gender", "isPrimaryApplicant", "lastName", "middleName", "nationality", "professionalDetails", "sourceOfFunds", "taxDetails", "title"]

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
    def from_json(cls, json_str: str) -> StakeholderDetails2:
        """Create an instance of StakeholderDetails2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of address
        if self.address:
            _dict['address'] = self.address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of contact_details
        if self.contact_details:
            _dict['contactDetails'] = self.contact_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of document_details
        if self.document_details:
            _dict['documentDetails'] = self.document_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in professional_details (list)
        _items = []
        if self.professional_details:
            for _item in self.professional_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['professionalDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StakeholderDetails2:
        """Create an instance of StakeholderDetails2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StakeholderDetails2.parse_obj(obj)

        _obj = StakeholderDetails2.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "address": ProductAddress.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "birth_country": obj.get("birthCountry"),
            "contact_details": ContactDetails.from_dict(obj.get("contactDetails")) if obj.get("contactDetails") is not None else None,
            "date_of_birth": obj.get("dateOfBirth"),
            "document_details": ProductDocumentDetail.from_dict(obj.get("documentDetails")) if obj.get("documentDetails") is not None else None,
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "is_primary_applicant": obj.get("isPrimaryApplicant"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "professional_details": [ProductProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "source_of_funds": obj.get("sourceOfFunds"),
            "tax_details": [ProductTaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "title": obj.get("title")
        })
        return _obj


