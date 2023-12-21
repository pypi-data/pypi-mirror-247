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
from nium.models.rfi_template import RfiTemplate

class ComplianceRFITemplateMetadataResponseDTO(BaseModel):
    """
    ComplianceRFITemplateMetadataResponseDTO
    """
    rfi_templates: Optional[conlist(RfiTemplate)] = Field(None, alias="rfiTemplates", description="This is an array object which contains the list of RFI template details.")
    __properties = ["rfiTemplates"]

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
    def from_json(cls, json_str: str) -> ComplianceRFITemplateMetadataResponseDTO:
        """Create an instance of ComplianceRFITemplateMetadataResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in rfi_templates (list)
        _items = []
        if self.rfi_templates:
            for _item in self.rfi_templates:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rfiTemplates'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplianceRFITemplateMetadataResponseDTO:
        """Create an instance of ComplianceRFITemplateMetadataResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceRFITemplateMetadataResponseDTO.parse_obj(obj)

        _obj = ComplianceRFITemplateMetadataResponseDTO.parse_obj({
            "rfi_templates": [RfiTemplate.from_dict(_item) for _item in obj.get("rfiTemplates")] if obj.get("rfiTemplates") is not None else None
        })
        return _obj


