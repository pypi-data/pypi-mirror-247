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
from nium.models.corporate_document_upload_business_details_dto import CorporateDocumentUploadBusinessDetailsDTO

class CorporateComplianceDocumentRequestDTO(BaseModel):
    """
    CorporateComplianceDocumentRequestDTO
    """
    business_details: Optional[CorporateDocumentUploadBusinessDetailsDTO] = Field(None, alias="businessDetails")
    region: Optional[StrictStr] = None
    __properties = ["businessDetails", "region"]

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
    def from_json(cls, json_str: str) -> CorporateComplianceDocumentRequestDTO:
        """Create an instance of CorporateComplianceDocumentRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of business_details
        if self.business_details:
            _dict['businessDetails'] = self.business_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateComplianceDocumentRequestDTO:
        """Create an instance of CorporateComplianceDocumentRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateComplianceDocumentRequestDTO.parse_obj(obj)

        _obj = CorporateComplianceDocumentRequestDTO.parse_obj({
            "business_details": CorporateDocumentUploadBusinessDetailsDTO.from_dict(obj.get("businessDetails")) if obj.get("businessDetails") is not None else None,
            "region": obj.get("region")
        })
        return _obj


