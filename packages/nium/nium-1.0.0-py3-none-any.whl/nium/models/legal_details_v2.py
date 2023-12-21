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

class LegalDetailsV2(BaseModel):
    """
    LegalDetailsV2
    """
    legislation_name: Optional[StrictStr] = Field(None, alias="legislationName")
    legislation_type: Optional[StrictStr] = Field(None, alias="legislationType")
    listed_exchange: Optional[StrictStr] = Field(None, alias="listedExchange")
    registered_country: Optional[StrictStr] = Field(None, alias="registeredCountry")
    registered_date: Optional[StrictStr] = Field(None, alias="registeredDate")
    registration_type: Optional[StrictStr] = Field(None, alias="registrationType")
    __properties = ["legislationName", "legislationType", "listedExchange", "registeredCountry", "registeredDate", "registrationType"]

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
    def from_json(cls, json_str: str) -> LegalDetailsV2:
        """Create an instance of LegalDetailsV2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LegalDetailsV2:
        """Create an instance of LegalDetailsV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LegalDetailsV2.parse_obj(obj)

        _obj = LegalDetailsV2.parse_obj({
            "legislation_name": obj.get("legislationName"),
            "legislation_type": obj.get("legislationType"),
            "listed_exchange": obj.get("listedExchange"),
            "registered_country": obj.get("registeredCountry"),
            "registered_date": obj.get("registeredDate"),
            "registration_type": obj.get("registrationType")
        })
        return _obj


