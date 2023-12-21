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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist

class RiskAssessmentInfoV2(BaseModel):
    """
    RiskAssessmentInfoV2
    """
    annual_turnover: Optional[StrictStr] = Field(None, alias="annualTurnover")
    country_of_operation: Optional[conlist(StrictStr)] = Field(None, alias="countryOfOperation")
    industry_sector: Optional[StrictStr] = Field(None, alias="industrySector")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount")
    ofac_licence_present: Optional[StrictBool] = Field(None, alias="ofacLicencePresent")
    restricted_countries: Optional[conlist(StrictStr)] = Field(None, alias="restrictedCountries")
    total_employees: Optional[StrictStr] = Field(None, alias="totalEmployees")
    transaction_countries: Optional[conlist(StrictStr)] = Field(None, alias="transactionCountries")
    travel_restricted_country: Optional[StrictBool] = Field(None, alias="travelRestrictedCountry")
    __properties = ["annualTurnover", "countryOfOperation", "industrySector", "intendedUseOfAccount", "ofacLicencePresent", "restrictedCountries", "totalEmployees", "transactionCountries", "travelRestrictedCountry"]

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
    def from_json(cls, json_str: str) -> RiskAssessmentInfoV2:
        """Create an instance of RiskAssessmentInfoV2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RiskAssessmentInfoV2:
        """Create an instance of RiskAssessmentInfoV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RiskAssessmentInfoV2.parse_obj(obj)

        _obj = RiskAssessmentInfoV2.parse_obj({
            "annual_turnover": obj.get("annualTurnover"),
            "country_of_operation": obj.get("countryOfOperation"),
            "industry_sector": obj.get("industrySector"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "ofac_licence_present": obj.get("ofacLicencePresent"),
            "restricted_countries": obj.get("restrictedCountries"),
            "total_employees": obj.get("totalEmployees"),
            "transaction_countries": obj.get("transactionCountries"),
            "travel_restricted_country": obj.get("travelRestrictedCountry")
        })
        return _obj


