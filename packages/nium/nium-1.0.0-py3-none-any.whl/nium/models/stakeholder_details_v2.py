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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist
from nium.models.address_v2 import AddressV2
from nium.models.corporate_document_details2_dto import CorporateDocumentDetails2DTO
from nium.models.professional_details_response_dto import ProfessionalDetailsResponseDTO
from nium.models.stakeholder_contact_details_response_dto import StakeholderContactDetailsResponseDTO
from nium.models.tax_details_response_dto import TaxDetailsResponseDTO

class StakeholderDetailsV2(BaseModel):
    """
    StakeholderDetailsV2
    """
    address: Optional[AddressV2] = None
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry")
    contact_details: Optional[StakeholderContactDetailsResponseDTO] = Field(None, alias="contactDetails")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth")
    document_details: Optional[conlist(CorporateDocumentDetails2DTO)] = Field(None, alias="documentDetails")
    first_name: Optional[StrictStr] = Field(None, alias="firstName")
    gender: Optional[StrictStr] = None
    is_pep: Optional[StrictBool] = Field(None, alias="isPep")
    last_name: Optional[StrictStr] = Field(None, alias="lastName")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName")
    nationality: Optional[StrictStr] = None
    professional_details: Optional[conlist(ProfessionalDetailsResponseDTO)] = Field(None, alias="professionalDetails")
    tax_details: Optional[conlist(TaxDetailsResponseDTO)] = Field(None, alias="taxDetails")
    __properties = ["address", "birthCountry", "contactDetails", "dateOfBirth", "documentDetails", "firstName", "gender", "isPep", "lastName", "middleName", "nationality", "professionalDetails", "taxDetails"]

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
    def from_json(cls, json_str: str) -> StakeholderDetailsV2:
        """Create an instance of StakeholderDetailsV2 from a JSON string"""
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
    def from_dict(cls, obj: dict) -> StakeholderDetailsV2:
        """Create an instance of StakeholderDetailsV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StakeholderDetailsV2.parse_obj(obj)

        _obj = StakeholderDetailsV2.parse_obj({
            "address": AddressV2.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "birth_country": obj.get("birthCountry"),
            "contact_details": StakeholderContactDetailsResponseDTO.from_dict(obj.get("contactDetails")) if obj.get("contactDetails") is not None else None,
            "date_of_birth": obj.get("dateOfBirth"),
            "document_details": [CorporateDocumentDetails2DTO.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "is_pep": obj.get("isPep"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "professional_details": [ProfessionalDetailsResponseDTO.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "tax_details": [TaxDetailsResponseDTO.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None
        })
        return _obj


