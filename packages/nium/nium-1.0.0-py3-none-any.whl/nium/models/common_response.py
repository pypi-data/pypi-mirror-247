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
from nium.models.error_code_mapping import ErrorCodeMapping

class CommonResponse(BaseModel):
    """
    CommonResponse
    """
    status: Optional[StrictStr] = None
    message: Optional[StrictStr] = None
    error_details: Optional[conlist(ErrorCodeMapping)] = Field(None, alias="errorDetails")
    errors: Optional[conlist(StrictStr)] = None
    __properties = ["status", "message", "errorDetails", "errors"]

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
    def from_json(cls, json_str: str) -> CommonResponse:
        """Create an instance of CommonResponse from a JSON string"""
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
    def from_dict(cls, obj: dict) -> CommonResponse:
        """Create an instance of CommonResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CommonResponse.parse_obj(obj)

        _obj = CommonResponse.parse_obj({
            "status": obj.get("status"),
            "message": obj.get("message"),
            "error_details": [ErrorCodeMapping.from_dict(_item) for _item in obj.get("errorDetails")] if obj.get("errorDetails") is not None else None,
            "errors": obj.get("errors")
        })
        return _obj


