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
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.corporate_business_details_document_detail_dto import CorporateBusinessDetailsDocumentDetailDTO
from nium.models.corporate_document_upload_applicant_details_dto import CorporateDocumentUploadApplicantDetailsDTO
from nium.models.corporate_document_upload_stakeholders_dto import CorporateDocumentUploadStakeholdersDTO

class CorporateDocumentUploadBusinessDetailsDTO(BaseModel):
    """
    CorporateDocumentUploadBusinessDetailsDTO
    """
    applicant_details: Optional[CorporateDocumentUploadApplicantDetailsDTO] = Field(None, alias="applicantDetails")
    document_details: Optional[conlist(CorporateBusinessDetailsDocumentDetailDTO)] = Field(None, alias="documentDetails")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId")
    stakeholders: Optional[conlist(CorporateDocumentUploadStakeholdersDTO)] = None
    __properties = ["applicantDetails", "documentDetails", "referenceId", "stakeholders"]

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
    def from_json(cls, json_str: str) -> CorporateDocumentUploadBusinessDetailsDTO:
        """Create an instance of CorporateDocumentUploadBusinessDetailsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of applicant_details
        if self.applicant_details:
            _dict['applicantDetails'] = self.applicant_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in stakeholders (list)
        _items = []
        if self.stakeholders:
            for _item in self.stakeholders:
                if _item:
                    _items.append(_item.to_dict())
            _dict['stakeholders'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateDocumentUploadBusinessDetailsDTO:
        """Create an instance of CorporateDocumentUploadBusinessDetailsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateDocumentUploadBusinessDetailsDTO.parse_obj(obj)

        _obj = CorporateDocumentUploadBusinessDetailsDTO.parse_obj({
            "applicant_details": CorporateDocumentUploadApplicantDetailsDTO.from_dict(obj.get("applicantDetails")) if obj.get("applicantDetails") is not None else None,
            "document_details": [CorporateBusinessDetailsDocumentDetailDTO.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "stakeholders": [CorporateDocumentUploadStakeholdersDTO.from_dict(_item) for _item in obj.get("stakeholders")] if obj.get("stakeholders") is not None else None
        })
        return _obj


