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
from pydantic import BaseModel, Field
from nium.models.button_dto import ButtonDTO
from nium.models.container_dto import ContainerDTO
from nium.models.input_field_dto import InputFieldDTO

class CSSAttributeDTO(BaseModel):
    """
    CSSAttributeDTO
    """
    button: Optional[ButtonDTO] = None
    container: Optional[ContainerDTO] = None
    input_field: Optional[InputFieldDTO] = Field(None, alias="inputField")
    __properties = ["button", "container", "inputField"]

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
    def from_json(cls, json_str: str) -> CSSAttributeDTO:
        """Create an instance of CSSAttributeDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of button
        if self.button:
            _dict['button'] = self.button.to_dict()
        # override the default output from pydantic by calling `to_dict()` of container
        if self.container:
            _dict['container'] = self.container.to_dict()
        # override the default output from pydantic by calling `to_dict()` of input_field
        if self.input_field:
            _dict['inputField'] = self.input_field.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CSSAttributeDTO:
        """Create an instance of CSSAttributeDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CSSAttributeDTO.parse_obj(obj)

        _obj = CSSAttributeDTO.parse_obj({
            "button": ButtonDTO.from_dict(obj.get("button")) if obj.get("button") is not None else None,
            "container": ContainerDTO.from_dict(obj.get("container")) if obj.get("container") is not None else None,
            "input_field": InputFieldDTO.from_dict(obj.get("inputField")) if obj.get("inputField") is not None else None
        })
        return _obj


