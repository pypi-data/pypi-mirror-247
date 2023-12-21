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

class StakeholderContactDetailsResponseDTO(BaseModel):
    """
    StakeholderContactDetailsResponseDTO
    """
    contact_no: Optional[StrictStr] = Field(None, alias="contactNo")
    email: Optional[StrictStr] = None
    __properties = ["contactNo", "email"]

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
    def from_json(cls, json_str: str) -> StakeholderContactDetailsResponseDTO:
        """Create an instance of StakeholderContactDetailsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StakeholderContactDetailsResponseDTO:
        """Create an instance of StakeholderContactDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StakeholderContactDetailsResponseDTO.parse_obj(obj)

        _obj = StakeholderContactDetailsResponseDTO.parse_obj({
            "contact_no": obj.get("contactNo"),
            "email": obj.get("email")
        })
        return _obj


