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
from pydantic import BaseModel, Field, conlist
from nium.models.document_detail import DocumentDetail

class CorporateDocumentUploadStakeholderDetailsDTO(BaseModel):
    """
    CorporateDocumentUploadStakeholderDetailsDTO
    """
    document_details: Optional[conlist(DocumentDetail)] = Field(None, alias="documentDetails")
    __properties = ["documentDetails"]

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
    def from_json(cls, json_str: str) -> CorporateDocumentUploadStakeholderDetailsDTO:
        """Create an instance of CorporateDocumentUploadStakeholderDetailsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateDocumentUploadStakeholderDetailsDTO:
        """Create an instance of CorporateDocumentUploadStakeholderDetailsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateDocumentUploadStakeholderDetailsDTO.parse_obj(obj)

        _obj = CorporateDocumentUploadStakeholderDetailsDTO.parse_obj({
            "document_details": [DocumentDetail.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None
        })
        return _obj


