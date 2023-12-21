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

class CvvResponseDTO(BaseModel):
    """
    CvvResponseDTO
    """
    cvv: Optional[StrictStr] = Field(None, description="This field contains the 3-digit Base64 encoded CVV for the card.")
    expiry: Optional[StrictStr] = Field(None, description="This field contains the Base64 encoded expiry date of the card in YYMM format.")
    __properties = ["cvv", "expiry"]

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
    def from_json(cls, json_str: str) -> CvvResponseDTO:
        """Create an instance of CvvResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CvvResponseDTO:
        """Create an instance of CvvResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CvvResponseDTO.parse_obj(obj)

        _obj = CvvResponseDTO.parse_obj({
            "cvv": obj.get("cvv"),
            "expiry": obj.get("expiry")
        })
        return _obj


