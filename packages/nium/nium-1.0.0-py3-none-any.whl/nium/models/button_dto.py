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

class ButtonDTO(BaseModel):
    """
    ButtonDTO
    """
    border_color: Optional[StrictStr] = Field(None, alias="borderColor", description="This field accepts the client card widget style for button border color.")
    color: Optional[StrictStr] = Field(None, description="This field accepts the client card widget style for button color.")
    font_size: Optional[StrictStr] = Field(None, alias="fontSize", description="This field accepts the client card widget style for button font size.")
    text_color: Optional[StrictStr] = Field(None, alias="textColor", description="This field accepts the client card widget style for button text color.")
    __properties = ["borderColor", "color", "fontSize", "textColor"]

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
    def from_json(cls, json_str: str) -> ButtonDTO:
        """Create an instance of ButtonDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ButtonDTO:
        """Create an instance of ButtonDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ButtonDTO.parse_obj(obj)

        _obj = ButtonDTO.parse_obj({
            "border_color": obj.get("borderColor"),
            "color": obj.get("color"),
            "font_size": obj.get("fontSize"),
            "text_color": obj.get("textColor")
        })
        return _obj


