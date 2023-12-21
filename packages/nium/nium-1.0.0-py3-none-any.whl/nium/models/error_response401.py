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
from pydantic import BaseModel, Field, conlist
from nium.models.error_detail401 import ErrorDetail401

class ErrorResponse401(BaseModel):
    """
    ErrorResponse401
    """
    error_details: Optional[conlist(ErrorDetail401)] = Field(None, alias="errorDetails")
    __properties = ["errorDetails"]

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
    def from_json(cls, json_str: str) -> ErrorResponse401:
        """Create an instance of ErrorResponse401 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in error_details (list)
        _items = []
        if self.error_details:
            for _item in self.error_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['errorDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ErrorResponse401:
        """Create an instance of ErrorResponse401 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ErrorResponse401.parse_obj(obj)

        _obj = ErrorResponse401.parse_obj({
            "error_details": [ErrorDetail401.from_dict(_item) for _item in obj.get("errorDetails")] if obj.get("errorDetails") is not None else None
        })
        return _obj


