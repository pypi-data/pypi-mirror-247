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
from pydantic import BaseModel, StrictStr

class BranchNameResponseDTO(BaseModel):
    """
    BranchNameResponseDTO
    """
    city: Optional[StrictStr] = None
    district: Optional[StrictStr] = None
    ifsc: Optional[StrictStr] = None
    state: Optional[StrictStr] = None
    __properties = ["city", "district", "ifsc", "state"]

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
    def from_json(cls, json_str: str) -> BranchNameResponseDTO:
        """Create an instance of BranchNameResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BranchNameResponseDTO:
        """Create an instance of BranchNameResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BranchNameResponseDTO.parse_obj(obj)

        _obj = BranchNameResponseDTO.parse_obj({
            "city": obj.get("city"),
            "district": obj.get("district"),
            "ifsc": obj.get("ifsc"),
            "state": obj.get("state")
        })
        return _obj


