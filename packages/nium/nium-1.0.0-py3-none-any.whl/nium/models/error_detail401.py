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
from nium.models.error_codes401 import ErrorCodes401

class ErrorDetail401(BaseModel):
    """
    error details description  # noqa: E501
    """
    code: Optional[ErrorCodes401] = None
    description: Optional[StrictStr] = Field(None, description="Description of the error.")
    __properties = ["code", "description"]

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
    def from_json(cls, json_str: str) -> ErrorDetail401:
        """Create an instance of ErrorDetail401 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ErrorDetail401:
        """Create an instance of ErrorDetail401 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ErrorDetail401.parse_obj(obj)

        _obj = ErrorDetail401.parse_obj({
            "code": obj.get("code"),
            "description": obj.get("description")
        })
        return _obj


