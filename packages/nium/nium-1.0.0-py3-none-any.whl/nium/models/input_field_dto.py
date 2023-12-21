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

class InputFieldDTO(BaseModel):
    """
    InputFieldDTO
    """
    active_border_color: Optional[StrictStr] = Field(None, alias="activeBorderColor", description="This field accepts the client card widget style for text filed active border color.")
    error_border_color: Optional[StrictStr] = Field(None, alias="errorBorderColor", description="This field accepts the client card widget style for text filed error border color.")
    error_message_color: Optional[StrictStr] = Field(None, alias="errorMessageColor", description="This field accepts the client car d widget style for text filed error label color.")
    label_color: Optional[StrictStr] = Field(None, alias="labelColor", description="This field accepts the client card widget style for text filed label color.")
    label_font_size: Optional[StrictStr] = Field(None, alias="labelFontSize", description="This field accepts the client card widget style for text filed label size.")
    __properties = ["activeBorderColor", "errorBorderColor", "errorMessageColor", "labelColor", "labelFontSize"]

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
    def from_json(cls, json_str: str) -> InputFieldDTO:
        """Create an instance of InputFieldDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InputFieldDTO:
        """Create an instance of InputFieldDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InputFieldDTO.parse_obj(obj)

        _obj = InputFieldDTO.parse_obj({
            "active_border_color": obj.get("activeBorderColor"),
            "error_border_color": obj.get("errorBorderColor"),
            "error_message_color": obj.get("errorMessageColor"),
            "label_color": obj.get("labelColor"),
            "label_font_size": obj.get("labelFontSize")
        })
        return _obj


