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
from nium.models.corporate_address_dto import CorporateAddressDTO
from nium.models.corporate_document_details_dto import CorporateDocumentDetailsDTO
from nium.models.professional_details import ProfessionalDetails
from nium.models.tax_details import TaxDetails

class StakeholderDetailsResponseDTO(BaseModel):
    """
    StakeholderDetailsResponseDTO
    """
    address: Optional[CorporateAddressDTO] = None
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field contains the date of birth of the stakeholder.")
    designation: Optional[StrictStr] = Field(None, description="This field contains the designation of the stakeholder.")
    document_details: Optional[conlist(CorporateDocumentDetailsDTO)] = Field(None, alias="documentDetails")
    email: Optional[StrictStr] = Field(None, description="This field contains the email address of the stakeholder")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the stakeholder.")
    gender: Optional[StrictStr] = Field(None, description="This field contains the gender of the stakeholder.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the stakeholder.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the stakeholder.")
    mobile: Optional[StrictStr] = Field(None, description="This field contains the mobile number of the stakeholder")
    nationality: Optional[StrictStr] = Field(None, description="This field contains the nationality of the stakeholder.")
    professional_details: Optional[conlist(ProfessionalDetails)] = Field(None, alias="professionalDetails")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field contains the reference id of the stakeholder")
    resident: Optional[StrictBool] = None
    tax_details: Optional[conlist(TaxDetails)] = Field(None, alias="taxDetails")
    __properties = ["address", "birthCountry", "dateOfBirth", "designation", "documentDetails", "email", "firstName", "gender", "lastName", "middleName", "mobile", "nationality", "professionalDetails", "referenceId", "resident", "taxDetails"]

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
    def from_json(cls, json_str: str) -> StakeholderDetailsResponseDTO:
        """Create an instance of StakeholderDetailsResponseDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> StakeholderDetailsResponseDTO:
        """Create an instance of StakeholderDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StakeholderDetailsResponseDTO.parse_obj(obj)

        _obj = StakeholderDetailsResponseDTO.parse_obj({
            "address": CorporateAddressDTO.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "birth_country": obj.get("birthCountry"),
            "date_of_birth": obj.get("dateOfBirth"),
            "designation": obj.get("designation"),
            "document_details": [CorporateDocumentDetailsDTO.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "email": obj.get("email"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "mobile": obj.get("mobile"),
            "nationality": obj.get("nationality"),
            "professional_details": [ProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "resident": obj.get("resident"),
            "tax_details": [TaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None
        })
        return _obj


