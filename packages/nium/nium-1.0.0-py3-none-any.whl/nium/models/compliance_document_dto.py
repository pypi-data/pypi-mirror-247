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
from nium.models.compliance_identification_doc_dto import ComplianceIdentificationDocDTO

class ComplianceDocumentDTO(BaseModel):
    """
    ComplianceDocumentDTO
    """
    identification_doc: Optional[conlist(ComplianceIdentificationDocDTO)] = Field(None, alias="identificationDoc", description="This field is an array which accepts document objects. Total size of the array should be less than 10 MB.")
    __properties = ["identificationDoc"]

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
    def from_json(cls, json_str: str) -> ComplianceDocumentDTO:
        """Create an instance of ComplianceDocumentDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in identification_doc (list)
        _items = []
        if self.identification_doc:
            for _item in self.identification_doc:
                if _item:
                    _items.append(_item.to_dict())
            _dict['identificationDoc'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplianceDocumentDTO:
        """Create an instance of ComplianceDocumentDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceDocumentDTO.parse_obj(obj)

        _obj = ComplianceDocumentDTO.parse_obj({
            "identification_doc": [ComplianceIdentificationDocDTO.from_dict(_item) for _item in obj.get("identificationDoc")] if obj.get("identificationDoc") is not None else None
        })
        return _obj


