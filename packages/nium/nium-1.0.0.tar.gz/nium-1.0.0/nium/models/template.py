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
from nium.models.required_fields import RequiredFields

class Template(BaseModel):
    """
    Template
    """
    document_type: Optional[StrictStr] = Field(None, alias="documentType", description="This field contains the RFI document type. The possible values are: POA POI")
    name: Optional[StrictStr] = Field(None, description="This field contains name of the RFI template.")
    required_fields: Optional[conlist(RequiredFields)] = Field(None, alias="requiredFields", description="This is an array which contains the list of fields for the RFI template.")
    rfi_type: Optional[StrictStr] = Field(None, alias="rfiType", description="This field contains the entity type for which the RFI is raised. The possible values are: corporate applicant stakeholder")
    type: Optional[StrictStr] = Field(None, description="This field contains the RFI template type. It can be either Data RFI or Document RFI. The possible values are: data document")
    __properties = ["documentType", "name", "requiredFields", "rfiType", "type"]

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
    def from_json(cls, json_str: str) -> Template:
        """Create an instance of Template from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in required_fields (list)
        _items = []
        if self.required_fields:
            for _item in self.required_fields:
                if _item:
                    _items.append(_item.to_dict())
            _dict['requiredFields'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Template:
        """Create an instance of Template from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Template.parse_obj(obj)

        _obj = Template.parse_obj({
            "document_type": obj.get("documentType"),
            "name": obj.get("name"),
            "required_fields": [RequiredFields.from_dict(_item) for _item in obj.get("requiredFields")] if obj.get("requiredFields") is not None else None,
            "rfi_type": obj.get("rfiType"),
            "type": obj.get("type")
        })
        return _obj


