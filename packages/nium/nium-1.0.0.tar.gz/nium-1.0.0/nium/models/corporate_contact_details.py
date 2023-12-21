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

class CorporateContactDetails(BaseModel):
    """
    CorporateContactDetails
    """
    contact_no: Optional[StrictStr] = Field(None, alias="contactNo", description="This field accepts the mobile number of the stakeholder for the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode")
    email: Optional[StrictStr] = Field(None, description="This field accepts the email address of the stakeholder for the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    __properties = ["contactNo", "countryCode", "email"]

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
    def from_json(cls, json_str: str) -> CorporateContactDetails:
        """Create an instance of CorporateContactDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateContactDetails:
        """Create an instance of CorporateContactDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateContactDetails.parse_obj(obj)

        _obj = CorporateContactDetails.parse_obj({
            "contact_no": obj.get("contactNo"),
            "country_code": obj.get("countryCode"),
            "email": obj.get("email")
        })
        return _obj


