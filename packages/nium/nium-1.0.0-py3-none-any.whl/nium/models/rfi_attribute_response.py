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

class RfiAttributeResponse(BaseModel):
    """
    RfiAttributeResponse
    """
    label: Optional[StrictStr] = Field(None, description="This field contains the user-friendly name of the RFI subfield that is required. For example, “Passport Number” when RFI is raised for POI(Passport) and passport number is needed.")
    type: Optional[StrictStr] = Field(None, description="This field contains the type of RFI which can be data or document.")
    value: Optional[StrictStr] = Field(None, description="This field contains the NIUM field value for the label, for example, identificationValue when passport number is needed.")
    __properties = ["label", "type", "value"]

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
    def from_json(cls, json_str: str) -> RfiAttributeResponse:
        """Create an instance of RfiAttributeResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RfiAttributeResponse:
        """Create an instance of RfiAttributeResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RfiAttributeResponse.parse_obj(obj)

        _obj = RfiAttributeResponse.parse_obj({
            "label": obj.get("label"),
            "type": obj.get("type"),
            "value": obj.get("value")
        })
        return _obj


