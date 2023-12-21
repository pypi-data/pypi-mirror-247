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
from nium.models.template import Template

class RfiTemplate(BaseModel):
    """
    RfiTemplate
    """
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field contains the reference ID of the the entity for which the RFI is raised.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains the remarks entered by compliance while raising RFI.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status of the RFI. The possible values are: RFI_REQUESTED RFI_RESPONDED")
    template: Optional[Template] = None
    template_id: Optional[StrictStr] = Field(None, alias="templateId", description="This field contains the ID of the RFI template.")
    __properties = ["referenceId", "remarks", "status", "template", "templateId"]

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
    def from_json(cls, json_str: str) -> RfiTemplate:
        """Create an instance of RfiTemplate from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of template
        if self.template:
            _dict['template'] = self.template.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RfiTemplate:
        """Create an instance of RfiTemplate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RfiTemplate.parse_obj(obj)

        _obj = RfiTemplate.parse_obj({
            "reference_id": obj.get("referenceId"),
            "remarks": obj.get("remarks"),
            "status": obj.get("status"),
            "template": Template.from_dict(obj.get("template")) if obj.get("template") is not None else None,
            "template_id": obj.get("templateId")
        })
        return _obj


