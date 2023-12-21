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
from pydantic import BaseModel, StrictStr, validator

class Standard500Error(BaseModel):
    """
    Standard500Error
    """
    code: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    __properties = ["code", "description"]

    @validator('code')
    def code_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('internal_error', 'external_dependent_system_failed'):
            raise ValueError("must be one of enum values ('internal_error', 'external_dependent_system_failed')")
        return value

    @validator('description')
    def description_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('An internal error occurred'):
            raise ValueError("must be one of enum values ('An internal error occurred')")
        return value

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
    def from_json(cls, json_str: str) -> Standard500Error:
        """Create an instance of Standard500Error from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Standard500Error:
        """Create an instance of Standard500Error from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Standard500Error.parse_obj(obj)

        _obj = Standard500Error.parse_obj({
            "code": obj.get("code"),
            "description": obj.get("description")
        })
        return _obj


