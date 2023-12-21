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

class ApiError2(BaseModel):
    """
    ApiError2
    """
    errors: Optional[conlist(StrictStr)] = Field(None, description="List of errors occurred.")
    message: Optional[StrictStr] = Field(None, description="Error message descriptor.")
    __properties = ["errors", "message"]

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
    def from_json(cls, json_str: str) -> ApiError2:
        """Create an instance of ApiError2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ApiError2:
        """Create an instance of ApiError2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ApiError2.parse_obj(obj)

        _obj = ApiError2.parse_obj({
            "errors": obj.get("errors"),
            "message": obj.get("message")
        })
        return _obj


