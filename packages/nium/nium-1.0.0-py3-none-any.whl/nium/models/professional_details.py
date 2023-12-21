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

class ProfessionalDetails(BaseModel):
    """
    ProfessionalDetails
    """
    employment_industry: Optional[StrictStr] = Field(None, alias="employmentIndustry")
    employment_status: Optional[StrictStr] = Field(None, alias="employmentStatus")
    position: Optional[StrictStr] = None
    position_end_date: Optional[StrictStr] = Field(None, alias="positionEndDate")
    position_start_date: Optional[StrictStr] = Field(None, alias="positionStartDate")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage")
    __properties = ["employmentIndustry", "employmentStatus", "position", "positionEndDate", "positionStartDate", "sharePercentage"]

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
    def from_json(cls, json_str: str) -> ProfessionalDetails:
        """Create an instance of ProfessionalDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProfessionalDetails:
        """Create an instance of ProfessionalDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProfessionalDetails.parse_obj(obj)

        _obj = ProfessionalDetails.parse_obj({
            "employment_industry": obj.get("employmentIndustry"),
            "employment_status": obj.get("employmentStatus"),
            "position": obj.get("position"),
            "position_end_date": obj.get("positionEndDate"),
            "position_start_date": obj.get("positionStartDate"),
            "share_percentage": obj.get("sharePercentage")
        })
        return _obj


