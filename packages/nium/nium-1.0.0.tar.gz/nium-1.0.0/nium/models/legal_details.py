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

class LegalDetails(BaseModel):
    """
    LegalDetails
    """
    legislation_name: Optional[StrictStr] = Field(None, alias="legislationName", description="This field accepts the name of the legislation under which the corporate entity being onboarded was formed. This field is required in case the region is AU when the entity type [refer businessDetails.businessType] is Government Body.  AU: Optional EU: NA UK: NA SG: NA")
    legislation_type: Optional[StrictStr] = Field(None, alias="legislationType", description="This field accepts the type of the legislation under which the corporate entity being onboarded was formed. The acceptable values are: Established under commonwealth legislation Established under State Territory legislation Other  AU: Optional EU: NA UK: NA SG: NA")
    listed_exchange: Optional[StrictStr] = Field(None, alias="listedExchange", description="This field accepts the exchange where the business is listed. Refer to the Glossary of Listed Exchange: This field is required in case the entity type is \"Public Company\" (please refer to businessDetails.businessType).  AU: Optional EU: NA UK: NA SG: Optional")
    registered_country: Optional[StrictStr] = Field(None, alias="registeredCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the country.  AU: Required EU: Required UK: Required SG: Required")
    registered_date: Optional[StrictStr] = Field(None, alias="registeredDate", description="This field accepts the business registration date for the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    registration_type: Optional[StrictStr] = Field(None, alias="registrationType", description="This field accepts the registration type for the entity.  AU: Optional EU: NA UK: NA SG: NA")
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
    def from_json(cls, json_str: str) -> LegalDetails:
        """Create an instance of LegalDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LegalDetails:
        """Create an instance of LegalDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LegalDetails.parse_obj(obj)

        _obj = LegalDetails.parse_obj({
            "legislation_name": obj.get("legislationName"),
            "legislation_type": obj.get("legislationType"),
            "listed_exchange": obj.get("listedExchange"),
            "registered_country": obj.get("registeredCountry"),
            "registered_date": obj.get("registeredDate"),
            "registration_type": obj.get("registrationType")
        })
        return _obj


