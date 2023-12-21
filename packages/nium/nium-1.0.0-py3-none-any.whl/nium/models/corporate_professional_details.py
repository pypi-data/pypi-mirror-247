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

class CorporateProfessionalDetails(BaseModel):
    """
    CorporateProfessionalDetails
    """
    position: Optional[StrictStr] = Field(None, description="This field accepts the position of the stakeholder. The acceptable values are: Ultimate Beneficial Owners (UBO) Director Shareholder  AU: Required EU: Required UK: Required SG: Required")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage", description="This field accepts the percentage of shares held by stakeholder. Note: This field is required in case of UBO.  AU: NA EU: Optional UK: Optional SG: Optional")
    __properties = ["position", "sharePercentage"]

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
    def from_json(cls, json_str: str) -> CorporateProfessionalDetails:
        """Create an instance of CorporateProfessionalDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateProfessionalDetails:
        """Create an instance of CorporateProfessionalDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateProfessionalDetails.parse_obj(obj)

        _obj = CorporateProfessionalDetails.parse_obj({
            "position": obj.get("position"),
            "share_percentage": obj.get("sharePercentage")
        })
        return _obj


