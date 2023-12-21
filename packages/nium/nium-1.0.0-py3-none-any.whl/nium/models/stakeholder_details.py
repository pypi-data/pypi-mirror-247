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

class StakeholderDetails(BaseModel):
    """
    StakeholderDetails
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo")
    address: Optional[ProductAddress] = None
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry", description="This field accepts the birth country name of the stakeholder.  AU: NA EU: Required UK: NA SG: NA")
    contact_details: Optional[ContactDetails] = Field(None, alias="contactDetails")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field accepts the date of birth of the stakeholder in yyyy-MM-dd format.  AU: Optional EU: Required UK: Required SG: Required")
    document_details: Optional[conlist(ProductDocumentDetail)] = Field(None, alias="documentDetails", description="This array accepts the document details for the stakeholder. This field is required only if the documents are being uploaded.  AU: Optional EU: Conditional UK: Optional SG: Optional")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the stakeholder. The acceptable values are: Male Female  AU: Optional EU: NA UK: NA SG: NA")
    kyc_mode: Optional[StrictStr] = Field(None, alias="kycMode", description="This object accepts the desired mode to do the KYC of the individual stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the stakeholder.  AU: Optional EU: Optional UK: Optional SG: Optional")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the nationality of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    professional_details: Optional[conlist(ProductProfessionalDetails)] = Field(None, alias="professionalDetails", description="This array accepts the professional details of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    tax_details: Optional[conlist(ProductTaxDetails)] = Field(None, alias="taxDetails", description="This array accepts the tax details.  AU: NA EU: Required UK: NA SG: NA")
    __properties = ["additionalInfo", "address", "birthCountry", "contactDetails", "dateOfBirth", "documentDetails", "firstName", "gender", "kycMode", "lastName", "middleName", "nationality", "professionalDetails", "taxDetails"]

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
    def from_json(cls, json_str: str) -> StakeholderDetails:
        """Create an instance of StakeholderDetails from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
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
    def from_dict(cls, obj: dict) -> StakeholderDetails:
        """Create an instance of StakeholderDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StakeholderDetails.parse_obj(obj)

        _obj = StakeholderDetails.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "address": ProductAddress.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "birth_country": obj.get("birthCountry"),
            "contact_details": ContactDetails.from_dict(obj.get("contactDetails")) if obj.get("contactDetails") is not None else None,
            "date_of_birth": obj.get("dateOfBirth"),
            "document_details": [ProductDocumentDetail.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "kyc_mode": obj.get("kycMode"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "professional_details": [ProductProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "tax_details": [ProductTaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None
        })
        return _obj


