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

class ProductProfessionalDetails(BaseModel):
    """
    ProductProfessionalDetails
    """
    position: Optional[StrictStr] = Field(None, description="This field accepts the position of the stakeholder. The acceptable values are: Ultimate Beneficial Owners (UBO) Director Shareholder  AU: Required EU: Required UK: Required SG: Required")
    position_end_date: Optional[StrictStr] = Field(None, alias="positionEndDate", description="This field accepts the end date of the stakeholders position.  AU: NA EU: Required UK: NA SG: NA")
    position_start_date: Optional[StrictStr] = Field(None, alias="positionStartDate", description="This field accepts the start date of the stakeholders position.  AU: NA EU: Required UK: NA SG: NA")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage", description="This field accepts the percentage of shares held by stakeholder. Note: This field is required in case of UBO.  AU: NA EU: Optional UK: Optional SG: Optional")
    __properties = ["position", "positionEndDate", "positionStartDate", "sharePercentage"]

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
    def from_json(cls, json_str: str) -> ProductProfessionalDetails:
        """Create an instance of ProductProfessionalDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductProfessionalDetails:
        """Create an instance of ProductProfessionalDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductProfessionalDetails.parse_obj(obj)

        _obj = ProductProfessionalDetails.parse_obj({
            "position": obj.get("position"),
            "position_end_date": obj.get("positionEndDate"),
            "position_start_date": obj.get("positionStartDate"),
            "share_percentage": obj.get("sharePercentage")
        })
        return _obj


