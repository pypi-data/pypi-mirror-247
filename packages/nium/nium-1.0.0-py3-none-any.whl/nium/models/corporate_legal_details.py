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

class CorporateLegalDetails(BaseModel):
    """
    CorporateLegalDetails
    """
    registered_country: Optional[StrictStr] = Field(None, alias="registeredCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the country.  AU: Required EU: Required UK: Required SG: Required")
    registered_date: Optional[StrictStr] = Field(None, alias="registeredDate", description="This field accepts the business registration date for the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    __properties = ["registeredCountry", "registeredDate"]

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
    def from_json(cls, json_str: str) -> CorporateLegalDetails:
        """Create an instance of CorporateLegalDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateLegalDetails:
        """Create an instance of CorporateLegalDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateLegalDetails.parse_obj(obj)

        _obj = CorporateLegalDetails.parse_obj({
            "registered_country": obj.get("registeredCountry"),
            "registered_date": obj.get("registeredDate")
        })
        return _obj


