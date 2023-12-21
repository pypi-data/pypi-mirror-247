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


from typing import Any, Optional
from pydantic import BaseModel, Field, StrictStr, validator

class FetchConversionError(BaseModel):
    """
    error details description   # noqa: E501
    """
    code: StrictStr = Field(..., description="The detailed error code associated with HTTP status 400. * `fx_constraint_violated_input`: The input violates the model constraints. ")
    description: StrictStr = Field(...)
    field: Optional[Any] = None
    __properties = ["code", "description", "field"]

    @validator('code')
    def code_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('fx_constraint_violated_input'):
            raise ValueError("must be one of enum values ('fx_constraint_violated_input')")
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
    def from_json(cls, json_str: str) -> FetchConversionError:
        """Create an instance of FetchConversionError from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if field (nullable) is None
        # and __fields_set__ contains the field
        if self.field is None and "field" in self.__fields_set__:
            _dict['field'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FetchConversionError:
        """Create an instance of FetchConversionError from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FetchConversionError.parse_obj(obj)

        _obj = FetchConversionError.parse_obj({
            "code": obj.get("code"),
            "description": obj.get("description"),
            "field": obj.get("field")
        })
        return _obj


